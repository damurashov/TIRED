#!/usr/bin/python3


import tired.ui
import time


def main():
    pass

if __name__ == "__main__":
    for i in range(50):
        time.sleep(0.02)
        tired.ui.print_progress(i, title="progress:", target=49, units='%')
