import os
import sys
import time
import threading

from model import Model as Embedding
from agent import Agent
 
def spinner():
    spinner = ['|', '/', '-', '\\']
    while True:
        for symbol in spinner:
            sys.stdout.write('\r' + symbol)
            sys.stdout.flush()
            time.sleep(0.1)


def run():
    
    agent = Agent()
    
    for line in sys.stdin:
        agent.question(line)

if __name__ == "__main__":
    run()