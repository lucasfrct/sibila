
from embedding import Embedding

class Agent:
	def __init__(self):
		self.embedding = Embedding()

	def question(self, question):
		answer = self.embedding.run(question)
		return answer