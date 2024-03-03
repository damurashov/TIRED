
import tired.logging
import time
import sys


if __name__ == "__main__":
    tired.logging.run_logging_server(port=int(sys.argv[1]))
