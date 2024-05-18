# flake8: noqa: E501

import sys

from src.utils.colors import colors
from src.utils import writer as Writer
from src.models.ollama import ModelOllama
from src.models.open_ai import ModelOpenAI
from src.modules.analyst.analyst import Analyst


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
        self.analyst = Analyst()

    def welcome(self):
        print("\n", f"{colors.WARNING}Como posso ajudar? {colors.ENDC}", "\n")

    def available(self):
        print("\n", f"{colors.WARNING}Quer perguntar mais alguma coisa? {colors.ENDC}", "\n") 

    def question(self, question):
        answer = self.openai.question(question, "")
        self.write(answer)
        self.available()
        return answer

    def write(self, content, delay=0.01):
        """ escreve a resposta num terminal com delay. """ 
        Writer.delay(content, delay)

    def run(self):
        self.welcome()
        for line in sys.stdin:
            self.question(line)

    def analyze(self):
        predic = self.analyst.predict()
        
        promt_errors = """"
        levante erros jurídicos ou pontos sensíveis de questionamento nessa cláusula se houver. me forneçao a resposta num formato json, com o campo tags, sendo este array com no mínimo 3 tags relacionadas a justificativa alegada, outro campo com a justificativa sendo uma string descrevendo o erro encontrado. Para cada erro sera uma objeto { tags: [], justificativa: ''}. 
        """
        answer = self.openai.question(promt_errors, predic) 
        self.write(answer)
