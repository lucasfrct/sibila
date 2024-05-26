from collections import defaultdict, Counter
from typing import List

import nltk
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

from src.agent.preprocessor import PreProcessor


class FeatureExtractor:
    def __init__(self):

        nltk.download('maxent_ne_chunker')

        self.preprocessor = PreProcessor()
        self.vectorizer = CountVectorizer()
        self.tfidf_vectorizer = TfidfVectorizer()

        self.vocabulary_tfidf = None
        self.vocabulary = None
        self.entities = None
        self.ngramas = None
        self.tags = None

        self.vocabulary_tfidf_list = []
        self.bag_words_matrix = []
        self.tfidf_matrix = []
        self.ctx_ngrams = []
        self.entity = []
        self.tag = []

    def syntax_analisys(self, text: str = ""):
        """ aplica análise sintática para retira do texto plavras chaves, tags e entidades. """  # noqa: E501

        digest = self.preprocessor.digest(text)

        # descobre as tags e entidades do texto
        self.tags = pos_tag(digest['tokens'])
        self.entities = ne_chunk(self.tags)
        self.tag = [tag for tag, mark in self.tags]
        self.entity = [entity for entity, tag in self.entities]

        # popula o digest
        digest['entities'] = self.entities
        digest['entity'] = self.entity
        digest['tags'] = self.tags
        digest['tag'] = self.tag

        return digest

    def window_context(self, text: str = "", window_size=2):  # noqa: E501
        """ Gera n-gramas em torno de uma palavra-alvo com um tamanho de janela específico. """  # noqa: E501

        # aplica a análise sintpatica
        digest = self.syntax_analisys(text)
        tokens = digest['tokens']
        entities = digest['entity']

        # junta todos os tokens obtidios a té o momento
        tokens_expands = []
        tokens_expands.extend(tokens)
        tokens_expands.extend(digest['entity'])
        tokens_expands.extend(digest['lemma'])
        tokens_expands.extend(digest['tag'])

        # separa os indíces de tokens que sõa entidades
        target_indices = [i for i, token in enumerate(tokens_expands) if token in entities]  # noqa: E501

        # monta os n-gramas (palavras distrinuidas por nós)
        self.ctx_ngrams = []
        for index in target_indices:
            start = max(0, index - window_size)
            end = index + window_size + 1
            self.ctx_ngrams.append(tokens_expands[start:end])

        self.ngramas = self.cooccurrence_matrix(self.ctx_ngrams)

        # monta o vacabuláriodas bag words com base nos tokens
        vocabulary = self.bow(tokens_expands)
        # monta o vacabulário TFIDF
        vocabulary_tfidf = self.tfidf(text)

        # determina o tamanho da seleção de tokens do vacabulário
        size_tokens = len(tokens)
        size_vocabulary = int((size_tokens * 0.5) / 2)
        if size_vocabulary < 5:
            size_vocabulary = size_tokens

        # monta as palavras quentes do texto
        hot = {}
        max_items = self.max(vocabulary, size_vocabulary)
        for key, val in max_items.items():
            hot[key] = val

        min_items = self.min(vocabulary_tfidf, size_vocabulary)
        for key, val in min_items.items():
            hot[key] = val

        # popula o digest
        digest['hot'] = hot
        digest['ngramas'] = self.ngramas
        digest['vocabulary'] = vocabulary
        digest['vocabulary_tfidf'] = vocabulary_tfidf

        return digest

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

    def bow(self, tokens: List[str] = []):
        """ extrai a bag words. """  # noqa: E501

        # extrai a matrix de bag words
        bag_words = self.vectorizer.fit_transform(tokens)
        self.bag_words_matrix = bag_words.toarray()

        # extrai o vacabulário em volta do bag words
        self.vocabulary = self.vectorizer.vocabulary_
        return self.vocabulary

    def tfidf(self, text: str = ""):
        """ matrix de características TF-IDF(Term Frequency-Inverse Document Frequency)"""  # noqa: E501

        # Transformação dos documentos em uma matriz TF-IDF
        tfidf = self.tfidf_vectorizer.fit_transform([text])
        self.tfidf_matrix = tfidf.toarray()

        # Vocabulário com índices
        self.vocabulary_tfidf_list = self.tfidf_vectorizer.get_feature_names_out()   # noqa: E501

        # Monta um vocabulario de frequencia
        self.vocabulary_tfidf = {}
        for word, weight in zip(self.vocabulary_tfidf_list, self.tfidf_matrix[0]):   # noqa: E501
            self.vocabulary_tfidf[word] = weight

        return self.vocabulary_tfidf

    def min(self, vocabulary={}, size: int = 5):
        """ Extrai os items de menor valor """  # noqa: E501
        return dict(sorted(vocabulary.items(), key=lambda item: item[1])[:size])   # noqa: E501

    def max(self, vocabulary={}, size: int = 5):
        """ Extrai os items de maior valor """  # noqa: E501
        return dict(sorted(vocabulary.items(), key=lambda item: item[1], reverse=True)[:size])   # noqa: E501
