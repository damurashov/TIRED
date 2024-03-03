import dataclasses
import json
import socket
import socketserver
import threading
import tired
import tired.datetime
import tired.meta
import tired.parse


_LOG_SECTION_DELIMETER = "-"
NONE = 0
ERROR = 1
WARNING = 2
INFO = 3
DEBUG = 4
LOG_LEVEL_TO_STRING_MAPPING = {
    ERROR: "E",
    WARNING: "W",
    INFO: "I",
    DEBUG: "D"
}
_LEVEL = INFO


class NetworkLoggingMessage(dict):
    @staticmethod
    def from_str(json_string: str):
        try:
            return NetworkLoggingMessage(json.loads(json_string))
        except Exception:
            return NetworkLoggingMessage()

    @staticmethod
    def from_bytes(json_bytes, encoding='utf-8'):
        try:
            ret = str(json_bytes, encoding).strip()

            return ret
        except Exception as e:
            return NetworkLoggingMessage()

    @staticmethod
    def make_response_from_payload(payload, timestamp=None):
        ret = NetworkLoggingMessage({"msgid": "response", "payload": payload})

        if timestamp:
            ret["counter"] = timestamp

        return ret

    @staticmethod
    def make_write_request_from_payload(payload):
        return NetworkLoggingMessage({"msgid": "write", "payload": payload})

    @staticmethod
    def make_read_request(timestamp=None):
        request = NetworkLoggingMessage({"msgid": "read"})

        if timestamp is not None:
            request["timestamp"] = timestamp

        return request

    def as_str(self):
        return json.dumps(self) + '\n'

    def as_bytes(self):
        return bytes(self.as_str(), 'utf-8')

    def is_read(self):
        return self.get("msgid", None) == "read"

    def is_write(self):
        return self.get("msgid", None) == "write"

    def is_response(self):
        return self.get("msgid", None) == "response"

    def try_get_payload(self):
        return self.get("payload", None)

    def try_get_timestamp(self):
        return self.get("timestamp", None)


@dataclasses.dataclass
class _CountedQueueItem:
    timestamp: object
    item: object


@dataclasses.dataclass
class _CountedQueue:
    """ Stores entries decodated w/ either timestamp, or a counter """
    max_size = 4096
    _queue = list()

    _counter = 0
    """ Helps distinguishing obsolete entries during requests """

    def push(self, item, timestamp=None):
        if timestamp is None:
            timestamp = self._counter

        self._queue.append(_CountedQueueItem(timestamp, item))
        self._counter += 1
        self._curtail()

    def _curtail(self):
        if len(self._queue) > self.max_size:
            self._queue = self._queue[-self.max_size - 1:]

    def iter(self, timestamp=None):
        if timestamp is None:
            yield from self._queue
        else:
            yield from filter(lambda i: i.timestamp == timestamp, self._queue)


class NetworkLoggingHandler(socketserver.BaseRequestHandler):
    _queue = _CountedQueue()
    _lock = threading.Lock()

    def append_to_queue(self, item: str):
        self._queue.push(item)

    def handle(self):
        """ https://docs.python.org/3.7/library/socketserver.html#socketserver.StreamRequestHandler """
        self.data = str(self.request.recv(1024).strip(), 'utf-8')
        request = NetworkLoggingMessage.from_str(self.data)

        if request.is_read():
            # Handle read request
            self._lock.acquire()

            # Queue items after timestamp (if one is present in the request)
            for item in self._queue.iter(request.try_get_timestamp()):
                # pack
                response = NetworkLoggingMessage.make_response_from_payload(item.item, item.timestamp)

                # send
                try:
                    self.request.sendall(response.as_bytes())
                except ConnectionResetError as e:
                    pass
                except BrokenPipeError as e:
                    pass

            self._lock.release()
        elif request.is_write():
            self._lock.acquire()
            payload = request.try_get_payload()

            if payload:
                self.append_to_queue(payload)

            self._lock.release()
        else:
            # Handle raw read request (just dump the items)
            print('got read (raw)')
            self._lock.acquire()

            for item in self._queue.iter():
                # send raw
                try:
                    self.request.sendall(bytes(item.item, 'utf-8'))
                except Exception as e:
                    pass

            self._lock.release()

    def send(data):
        data = NetworkLoggingMessage.make_write_request_from_payload(data).as_str()

        # Create a socket (SOCK_STREAM means a TCP socket)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                # Connect to server and send data
                sock.connect((self.host, self.port))
                sock.sendall(bytes(data + "\n", "utf-8"))
            except ConnectionRefusedError as e:
                pass
            except BrokenPipeError as e:
                pass


class NetworkLoggingServer:
    instance = None

    @staticmethod
    def get_instance(host=None, port=None):
        if NetworkLoggingServer.instance is None:
            if host is None or port is None:
                raise ValueError(f'Incorrect host/port pair ({host},{port})')

            NetworkLoggingServer.instance = NetworkLoggingServer(host, port)

        return NetworkLoggingServer.instance

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def get_host(self):
        return self.host

    def get_port(self):
        return self.port

    def send(self, data):
        data = NetworkLoggingMessage.make_write_request_from_payload(data).as_str()

        # Create a socket (SOCK_STREAM means a TCP socket)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                # Connect to server and send data
                sock.connect((self.host, self.port))
                sock.sendall(bytes(data + "\n", "utf-8"))
            except ConnectionRefusedError as e:
                pass
            except BrokenPipeError as e:
                pass

    def run(self, host='localhost', port=8080):
        with socketserver.TCPServer((self.host, self.port), NetworkLoggingHandler) as server:
            server.serve_forever()

    def send_message(self, level, context, *args):
        global _LOG_SECTION_DELIMETER
        global LOG_LEVEL_TO_STRING_MAPPING
        message = ' '.join(args)
        output = ' '.join([LOG_LEVEL_TO_STRING_MAPPING[level], _LOG_SECTION_DELIMETER,
            f"{tired.datetime.get_today_time_milliseconds_string()}", f"[{context}]", _LOG_SECTION_DELIMETER, message])
        self.send(output)



def default_printer(level, context, *args):
    message = ' '.join(args)
    output = ' '.join([LOG_LEVEL_TO_STRING_MAPPING[level], _LOG_SECTION_DELIMETER,
        f"{tired.datetime.get_today_time_milliseconds_string()}", f"[{context}]", _LOG_SECTION_DELIMETER, message])
    print(output)


_PRINTER = default_printer


def set_printer_remote_logging_server(host="localhost", port=8010):
    instance = NetworkLoggingServer.get_instance(host=host, port=port)
    global _PRINTER
    _PRINTER = instance.send_message


def run_logging_server(host="localhost", port=8010):
    """ Won't return """
    NetworkLoggingServer.get_instance(host, port).run()


def iter_connect_read_printer_network(counter, read_counter=4096):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            # Connect to server and send data
            sock.connect((NetworkLoggingServer.get_instance().get_host(), NetworkLoggingServer.get_instance().get_port()))
            request = NetworkLoggingMessage.make_read_request(timestamp=counter)
            sock.send(request.as_bytes())

            while True:
                read = str(sock.recv(read_counter), 'utf-8')

                if len(read) == 0:
                    return None
                else:
                    for line in tired.parse.iterate_string_multiline(read):
                        result = NetworkLoggingMessage.from_str(line)

                        if result.is_response:
                            yield result

                            return

                    return None
        except ConnectionRefusedError as e:
            pass


def default_filter(level, context, *args) -> bool:
    """ Returns True, when printing is allowed """
    global _LEVEL

    return level <= _LEVEL

_FILTER = default_filter

def _log_impl(level, *args):
    global _FILTER
    global _PRINTER

    context = tired.meta.get_stack_context_string(3)

    if _FILTER(level, context, *args):
        _PRINTER(level, context, *args)

def debug(*args):
    _log_impl(DEBUG, *args)


def error(*args):
    _log_impl(ERROR, *args)


def info(*args):
    _log_impl(INFO, *args)


def warning(*args):
    _log_impl(WARNING, *args)
