# flake8: noqa: E501

from typing import List

import spacy

import nltk
from nltk.corpus import stopwords

from spellchecker import SpellChecker

from src.utils import string as Str


class PreProcessor:
    def __init__(self, text: str = ""):

        nltk.download('averaged_perceptron_tagger')
        nltk.download('punkt')
        
        nltk.download('stopwords')
        nltk.download('words')
        nltk.download('rslp')

        self.stop_words = set(stopwords.words('portuguese'))
        self.spell = SpellChecker(language='pt')
        self.stemmer = nltk.stem.RSLPStemmer()
        self.nlp = spacy.load('pt_core_news_sm')

        self.text = text

        self.tokenized_text_filtred: List[str] = []
        self.normalized_text: List[str] = []
        self.lemmarized_text: List[str] = []
        self.tokenized_text: List[str] = []
        self.stemmed_text: List[str] = []
        self.clean_text = ""

    def text_cleaning(self, text: str = "") -> str:
        """Limpa o texyo para processamento"""
        self.clean_text = Str.clean(text)
        return self.clean_text

    def tokenize(self, text: str = "") -> List[str]:
        self.tokenized_text = Str.tokenize(text)
        return self.tokenized_text

    def removal_stop_word(self, text: str = "") -> List[str]:
        self.tokenized_text_filtred = Str.removal_stopwords(text)
        return self.tokenized_text_filtred

    def normalize(self, text: str = "") -> List[str]:
        self.normalized_text = Str.normalize(text)
        return self.normalized_text

    def lemmatization(self, text: str = "") -> List[str]:
        self.lemmarized_text = Str.lemmatization(text)
        return self.lemmarized_text

    def stemming(self, tokens: List[str] = []) -> List[str]:
        self.stemmed_text = [self.stemmer.stem(str(word)) for word in tokens]
        return self.stemmed_text

    def digest(self, text: str = ""):
        text = self.text_cleaning(text)
        tokens = self.tokenize(text)
        tokens = self.removal_stop_word(tokens)
        tokens = self.normalize(tokens)
        lemma = self.lemmatization(tokens)
        stems = self.stemming(tokens)
        return {"tokens": tokens, "lemma": lemma, "stems": stems}  # noqa: E501
