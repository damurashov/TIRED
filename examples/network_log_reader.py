import tired.logging
import time
import sys


if __name__ == "__main__":
    port=int(sys.argv[1])
    tired.logging.set_printer_remote_logging_server(host="localhost", port=port)

    for i in range(1000):
        for message in tired.logging.iter_connect_read_printer_network(counter=i):
            print(message)
