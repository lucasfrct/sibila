from collections import defaultdict, Counter
from typing import List

import nltk
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk

from sklearn.feature_extraction.text import CountVectorizer

from src.agent.preprocessor import PreProcessor


class FeatureExtractor:
    def __init__(self):

        nltk.download('maxent_ne_chunker')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('maxent_ne_chunker')
        nltk.download('stopwords')
        nltk.download('punkt')
        nltk.download('words')

        self.preprocessor = PreProcessor()
        self.vectorizer = CountVectorizer()
        self.bag_word_genetare = None

    def syntax_analisys(self, text: str = ""):
        """ aplica análise sintática para retira do texto plavras chaves e entidades. """  # noqa: E501
        digest = self.preprocessor.digest(text)
        digest['tags'] = pos_tag(digest['tokens'])
        digest['entities'] = ne_chunk(digest['tags'])
        return digest

    def window_context(self, text: str = "", window_size=2):  # noqa: E501
        """ Gera n-gramas em torno de uma palavra-alvo com um tamanho de janela específico. """  # noqa: E501

        digest = self.syntax_analisys(text)
        tokens = digest['tokens']
        entities = [entity for entity, tag in digest['entities']]

        tokens_expands = []
        tokens_expands.extend(tokens)
        tokens_expands.extend(digest['lemma'])
        tokens_expands.extend(digest['stems'])

        target_indices = [i for i, token in enumerate(tokens_expands) if token in entities]  # noqa: E501
        context_ngrams = []

        for index in target_indices:
            start = max(0, index - window_size)
            end = index + window_size + 1
            context_ngrams.append(tokens_expands[start:end])

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

    def bag_words(self, text: str = ""):
        """ aplica análise sintática para retira do texto plavras chaves e entidades. """  # noqa: E501
        digest = self.syntax_analisys(text)
        
        tokens_expands = []
        tokens_expands.extend(digest['tokens'])
        tokens_expands.extend(digest['lemma'])
        tokens_expands.extend(digest['stems'])
        
        self.bag_word_genetare = self.vectorizer.fit_transform(tokens_expands)
        return self.vectorizer.vocabulary_
