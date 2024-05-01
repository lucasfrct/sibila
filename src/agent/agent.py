
import numpy as np
from typing import List
from collections import defaultdict, Counter

import nltk
from nltk.tag import pos_tag
from nltk.util import ngrams
from nltk.chunk import ne_chunk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

from src.utils.colors import colors
from src.utils import writer as Writer
from src.entities.ollama_model import OllamaModel
from src.document import retrieval as DocRetrieval
from src.entities.model_open_ai import ModelOpenAI
from src.agent.preprocessor import PreProcessor


# Coleta dos dados - rotular dados
# Pré processamento
# - limpeza do texto
# - tokenizaçao
# - remoçao de palavra de parada
# - normalização (acentuaçao, ortografia, conversão para minúsculas)
# - lemarizaçao (extrair radical da palavras [stem] e recupera o lema)
# Extraçao de características
# - bag of words
# - TF-IDF (Term Frequency-Inverse Document Frequency).
# - Embeddings de palavras
# Construção do Modelo

class Agent:

    def __init__(self):
        
        self.model_ollama = OllamaModel()
        self.model_open_ai = ModelOpenAI()
        self.preprocessor = PreProcessor()

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
        # tokens = self.tokenize(text)
        # return self.syntax_analisys(tokens)
        return self.preprocessor.normalize(self.preprocessor.tokenize(text))  # noqa: E501

    def tokenize(self, text: str = "") -> List[str]:
        """ transfoma o texto em tokens. """  # noqa: E501
        tokens = word_tokenize(text)
        tokens = [token for token in tokens if token.isalpha()]
        return [word for word in tokens if word not in self.stop_words]

    def syntax_analisys(self, tokens: List[str]):
        """ aplica a nálise sintática para retira do texto plavras chaves e entidades. """  # noqa: E501
        tags = pos_tag(tokens)
        entities = ne_chunk(tags)
        return (tags, entities)

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

    def window_context(self, text, target_word, window_size=2):
        """ Gera n-gramas em torno de uma palavra-alvo com um tamanho de janela específico. """  # noqa: E501

        tokens = word_tokenize(text, language='portuguese')
        stop_words_set = set(stopwords.words('portuguese'))

        tokens = [token for token in tokens if token.lower() not in stop_words_set]  # noqa: E501

        target_indices = [i for i, token in enumerate(tokens) if token.lower() == target_word.lower()]  # noqa: E501
        context_ngrams = []

        for index in target_indices:
            start = max(0, index - window_size)
            end = index + window_size + 1
            context_ngrams.append(tokens[start:end])

        return self.cooccurrence_matrix(context_ngrams)

    def cooccurrence_matrix(self, ngrams_ctx):
        """ Constrói uma matriz de co-ocorrência a partir de uma lista de n-gramas. """  # noqa: E501
        cooccurrence_counts = defaultdict(Counter)

        for ngram_ctx in ngrams_ctx:
            for i in range(len(ngram_ctx)):
                for j in range(len(ngram_ctx)):
                    if i != j:
                        distance = abs(i - j)
                        weight = 1.0 / distance  # Quanto menor a distância, maior o peso  # noqa: E501
                        cooccurrence_counts[ngram_ctx[i]][ngram_ctx[j]] += weight  # noqa: E501

        return dict(cooccurrence_counts)
