
import os
import sys
import time
import threading

from model import Model

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

class Agent:
	def __init__(self):
		self.model = Model()
		print("\n",f"{bcolors.WARNING}Como posso ajudar hoje?{bcolors.ENDC}", "\n")

	def question(self, question):
		answer = self.model.question(question)
		# answer = self.model.search(question)
		self.delay_write(answer)
		return answer

	def delay_write(self, content, delay=0.01):
    
		print(f"{bcolors.OKCYAN}------------------------------------------------------------------------------------------------------------------------------------------", "\n", end='', flush=True)
		print(f"{bcolors.BOLD}R: {bcolors.ENDC}{bcolors.OKCYAN}", end='', flush=True)
		
		for letter in content:
			print(letter, end='', flush=True)
			time.sleep(delay)
		
		print() 
		print(f"{bcolors.OKCYAN}------------------------------------------------------------------------------------------------------------------------------------------{bcolors.ENDC}")
		print("\n") 
    