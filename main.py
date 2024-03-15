import os
import sys
import time
import threading

from embedding import Embedding

def escrever_letra_por_letra(texto, delay=0.01):
    
    print(f"{bcolors.OKCYAN}------------------------------------------------------------------------------------------------------------------------------------------", "\n", end='', flush=True)
    print(f"{bcolors.BOLD}R: {bcolors.ENDC}{bcolors.OKCYAN}", end='', flush=True)
    
    for letra in texto:
        print(letra, end='', flush=True)
        time.sleep(delay)
    
    print() 
    print(f"{bcolors.OKCYAN}------------------------------------------------------------------------------------------------------------------------------------------{bcolors.ENDC}")
    print("\n") 
    
def spinner():
    spinner = ['|', '/', '-', '\\']
    while True:
        for symbol in spinner:
            sys.stdout.write('\r' + symbol)
            sys.stdout.flush()
            time.sleep(0.1)


def query(question):
    embedding = Embedding()
    answer = embedding.run(question)
    return answer

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    
def run():
    
    print("\n",f"{bcolors.WARNING}Como posso ajudar hoje?{bcolors.ENDC}", "\n")
    
    for line in sys.stdin:
        question = line
        answer = query(question)
        escrever_letra_por_letra(answer)
        

if __name__ == "__main__":
    run()