import tired.logging
import time


if __name__ == "__main__":
    server = tired.logging.set_printer_network()

    while True:
        tired.logging.info("Tick")
        time.sleep(1.0)
