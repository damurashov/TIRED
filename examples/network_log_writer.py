import tired.logging
import time
import sys


if __name__ == "__main__":
    tired.logging.set_printer_remote_logging_server(port=int(sys.argv[1]))

    while True:
        tired.logging.info("Tick")
        time.sleep(1.0)
