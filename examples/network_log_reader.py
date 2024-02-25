import tired.logging
import time
import sys


if __name__ == "__main__":
    for i in range(1000):
        for message in tired.logging.iter_connect_read_printer_network(port=int(sys.argv[1]), counter=i):
            print(message)
