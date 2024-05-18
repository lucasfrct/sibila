
import sys
from nltk.corpus import stopwords

import networkx as nx
import matplotlib.pyplot as plt

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

        self.stop_words = set(stopwords.words('portuguese'))

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

    def digest(self, text: str = ""):
        """ faz a digestão do texto. """  # noqa: E501
        return self.featureextractor.window_context(text)  # noqa: E501

    def plot(self, data):
        G = nx.DiGraph()

        # Adicionar as arestas ao grafo
        for node, edges in data.items():
            for adjacent, weight in edges.items():
                G.add_edge(node, adjacent, weight=weight)

        # Desenhar o grafo
        pos = nx.spring_layout(G)  # Layout para o grafo
        nx.draw(G, pos, with_labels=True, node_color='skyblue',
                node_size=1000, edge_color='k', linewidths=1, font_size=10)

        # Desenhar os pesos das arestas
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        plt.title('Grafo de Co-ocorrências')
        plt.show()

    def run(self):
        self.welcome()
        for line in sys.stdin:
            self.question(line)
