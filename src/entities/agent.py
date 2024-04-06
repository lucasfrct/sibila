
import os
import sys
import time
import threading

from src.entities.model import Model
from src.utils.colors import colors
from src.database import chromadb


class Agent:
	def __init__(self):
		self.model = Model()
		self.db = chromadb

		print("\n",f"{colors.WARNING} Como posso ajudar hoje? {colors.ENDC}", "\n")

	def question(self, question):
		question_embedings = self.model.embed(question)
		result = self.db.query(question_embedings)
		documents = self.model.query_to_docs(result)
		answer = self.model.question_gpt(question, documents)
		self.delay_write(answer)
		return answer

	def delay_write(self, content, delay=0.01):
    
		print(f"{colors.OKCYAN}------------------------------------------------------------------------------------------------------------------------------------------", "\n", end='', flush=True)
		print(f"{colors.BOLD}R: {colors.ENDC}{colors.OKCYAN}", end='', flush=True)
		
		for letter in content:
			print(letter, end='', flush=True)
			time.sleep(delay)
		
		print() 
		print(f"{colors.OKCYAN}------------------------------------------------------------------------------------------------------------------------------------------{colors.ENDC}")
		print("\n") 
    