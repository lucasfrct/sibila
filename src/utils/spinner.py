import sys
import time


def spinner():
    spinner = ['|', '/', '-', '\\']
    while True:
        for symbol in spinner:
            sys.stdout.write('\r' + symbol)
            sys.stdout.flush()
            time.sleep(0.1)