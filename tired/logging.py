import dataclasses
import socket
import json
import socketserver
import threading
import tired
import tired.datetime
import tired.meta


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
    def make_response_from_payload(payload):
        return NetworkLoggingMessage({"msgid": "response", "payload": payload})

    @staticmethod
    def make_write_request_from_payload(payload):
        return NetworkLoggingMessage({"msgid": "write", "payload": payload})

    def as_str(self):
        return json.dumps(self) + '\n'

    def as_bytes(self):
        return bytes(self.as_str(), 'utf-8')

    def is_read(self):
        return self.get("msgid", None) == "read"

    def is_write(self):
        return self.get("msgid", None) == "write"

    def try_get_payload(self):
        return self.get("payload", None)


class NetworkLoggingServer(socketserver.BaseRequestHandler):
    instance = None
    host = None
    port = None
    _queue = list()
    _lock = threading.Lock()

    @staticmethod
    def send(data):
        data = NetworkLoggingMessage.make_write_request_from_payload(data).as_str()

        # Create a socket (SOCK_STREAM means a TCP socket)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                # Connect to server and send data
                sock.connect((NetworkLoggingServer.host, NetworkLoggingServer.port))
                sock.sendall(bytes(data + "\n", "utf-8"))
            except ConnectionRefusedError as e:
                pass

    def append_to_queue(self, item: str):
        self._queue.append(item)

        if len(self._queue) > 4096:  # TODO magic
            self._queue = self._queue[-self.queue_size_items - 1:]  # XXX

    def handle(self):
        print('got request')
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        #self.data = self.rfile.readline().strip()
        #self.data = self.rfile.read().strip()
        self.data = str(self.request.recv(1024).strip(), 'utf-8')
        request = NetworkLoggingMessage.from_str(self.data)

        if request.is_read():
            self._lock.acquire()

            for item in self._queue:
                # pack
                response = NetworkLoggingMessage.make_response_from_payload(item)

                # send
                #self.wfile.write(response.as_str())
                self.request.sendall(response.as_bytes())

            self._lock.release()
        elif request.is_write():
            self._lock.acquire()
            payload = request.try_get_payload()

            if payload:
                self.append_to_queue(payload)

            self._lock.release()
        else:
            print('got read (raw)')
            self._lock.acquire()

            for item in self._queue:
                # send raw
                #self.wfile.write(item)
                self.request.sendall(bytes(item, 'utf-8'))

            self._lock.release()

    def run(self, host='localhost', port=8080):
        # Create the server, binding to localhost on port 9999
        with socketserver.TCPServer((NetworkLoggingServer.host, NetworkLoggingServer.port), NetworkLoggingServer) as server:
            # Activate the server; this will keep running until you
            # interrupt the program with Ctrl-C
            server.serve_forever()

    @staticmethod
    def send_message(level, context, *args):
        global _LOG_SECTION_DELIMETER
        global LOG_LEVEL_TO_STRING_MAPPING
        message = ' '.join(args)
        output = ' '.join([LOG_LEVEL_TO_STRING_MAPPING[level], _LOG_SECTION_DELIMETER,
            f"{tired.datetime.get_today_time_milliseconds_string()}", f"[{context}]", _LOG_SECTION_DELIMETER, message])
        NetworkLoggingServer.send(output)


def default_printer(level, context, *args):
    message = ' '.join(args)
    output = ' '.join([LOG_LEVEL_TO_STRING_MAPPING[level], _LOG_SECTION_DELIMETER,
        f"{tired.datetime.get_today_time_milliseconds_string()}", f"[{context}]", _LOG_SECTION_DELIMETER, message])
    print(output)


_PRINTER = default_printer


def set_printer_network(host="localhost", port=8080):

    if NetworkLoggingServer.instance is not None:
        return

    import threading
    global _PRINTER
    server = NetworkLoggingServer
    NetworkLoggingServer.host = host
    NetworkLoggingServer.port = port
    thread = threading.Thread(target=server.run, args=(host,port))
    NetworkLoggingServer.instance = thread
    NetworkLoggingServer.instance.start()
    _PRINTER = server.send_message


def connect_printer_network(host="localhost", port=8080):
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
