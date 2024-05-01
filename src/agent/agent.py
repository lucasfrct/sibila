
import nltk
from nltk.corpus import stopwords

from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

import networkx as nx
import matplotlib.pyplot as plt

from src.utils.colors import colors
from src.utils import writer as Writer
from src.entities.ollama_model import OllamaModel
from src.document import retrieval as DocRetrieval
from src.entities.model_open_ai import ModelOpenAI
from src.agent.preprocessor import PreProcessor
from src.agent.featureextractor import FeatureExtractor


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
# - bag of words
# - TF-IDF (Term Frequency-Inverse Document Frequency).
# - Embeddings de palavras

class Agent:

    def __init__(self):

        self.model_ollama = OllamaModel()
        self.model_open_ai = ModelOpenAI()
        self.preprocessor = PreProcessor()
        self.featureextractor = FeatureExtractor()

        nltk.download('averaged_perceptron_tagger')
        nltk.download('maxent_ne_chunker')
        nltk.download('stopwords')
        nltk.download('punkt')
        nltk.download('words')
        self.stop_words = set(stopwords.words('portuguese'))

    def welcome(self):
        print("\n", f"{colors.WARNING}Como posso ajudar? {colors.ENDC}", "\n")   # noqa: E501

    def available(self):
        print("\n", f"{colors.WARNING}Quer perguntar mais alguma coisa? {colors.ENDC}", "\n")  # noqa: E501

    def question(self, question):
        """ envia uma consulta para o banco. """  # noqa: E501
        docs = DocRetrieval.query(question)
        documents = DocRetrieval.to_text(docs)
        answer = self.model_open_ai.question(question, documents)
        self.write(answer)
        self.available()
        return answer

    def write(self, content, delay=0.01):
        """ escreve a resposta num terminal com delay. """  # noqa: E501
        Writer.delay(content, delay)

    def digest(self, text: str = ""):
        """ faz a digestão do texto. """  # noqa: E501
        return self.featureextractor.bag_words(text)  # noqa: E501

    def intentions(self, text: str = ""):
        """ descobre uma intençao no texto. """  # noqa: E501

        intentions = [
            "Enganar",
            "informar",
            "Entreter",
            "Instruir",
            "Persuadir",
            "Descrever",
            "Questionar",
            "Convocar ação",
            "Expressar sentimentos ou opiniões",
        ]

        texts = [
            "Quero comprar um bilhete de avião",
            "Qual é a previsão do tempo para amanhã?",
            "Preciso de uma receita de bolo"
        ]

        # Pré-processamento e extração de características
        vectorizer = TfidfVectorizer(stop_words='english')
        X = vectorizer.fit_transform(texts)

        # Dividir dados em treino e teste
        X_train, X_test, y_train, y_test = train_test_split(X, intentions, test_size=0.25, random_state=42)  # noqa: E501
        # Construção do modelo
        model = SVC(kernel='linear')
        model.fit(X_train, y_train)

        # Avaliação do modelo
        predictions = model.predict(X_test)
        return classification_report(y_test, predictions)

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
