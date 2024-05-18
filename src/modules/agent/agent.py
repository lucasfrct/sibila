
import sys

from src.utils.colors import colors
from src.utils import writer as Writer
from src.models.ollama import ModelOllama
from src.models.open_ai import ModelOpenAI


# Coleta dos dados - rotular dados
# Pré processamento
# - limpeza do texto
# - tokenizaçao
# - remoçao de palavra de parada
# - normalização (acentuaçao, ortografia, conversão para minúsculas)
# - lemarizaçao (extrair o lema da palavra)
# - stemming (extrair radical da palavras)
# Extraçao de características
# - análise sintática (tags e entidades)
# - janela de context (tags e entidades)
# - bag of words (matrix de )
# - TF-IDF (Term Frequency-Inverse Document Frequency).
# - Embeddings de palavras

class Agent:

    def __init__(self):

        self.ollama = ModelOllama()
        self.openai = ModelOpenAI()

    def welcome(self):
        print("\n", f"{colors.WARNING}Como posso ajudar? {colors.ENDC}", "\n")   # noqa: E501

    def available(self):
        print("\n", f"{colors.WARNING}Quer perguntar mais alguma coisa? {colors.ENDC}", "\n")  # noqa: E501

    def question(self, question):
        answer = self.openai.question(question, "")
        self.write(answer)
        self.available()
        return answer

    def write(self, content, delay=0.01):
        """ escreve a resposta num terminal com delay. """  # noqa: E501
        Writer.delay(content, delay)

    def run(self):
        self.welcome()
        for line in sys.stdin:
            self.question(line)
