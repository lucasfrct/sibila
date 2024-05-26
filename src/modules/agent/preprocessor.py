import re
import unidecode

from typing import List

import spacy

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from spellchecker import SpellChecker


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

        # Remover acentos usando unidecode
        text = unidecode.unidecode(text)

        # Remover sinais de pontuação e caracteres não alfanuméricos. Isso remove tudo exceto letras, números e espaços  # noqa: E501
        text = re.sub(r'[^\w\s]', '', text)

        # Remover espaços extras
        self.clean_text = re.sub(r'\s+', ' ', text).strip()

        return self.clean_text

    def tokenize(self, text: str = "") -> List[str]:
        tokens = word_tokenize(text)
        self.tokenized_text = [str(token) for token in tokens if token.isalpha()]  # noqa: E501
        return self.tokenized_text

    def removal_stop_word(self, tokens: List[str] = []) -> List[str]:
        self.tokenized_text_filtred = [word for word in tokens if word not in self.stop_words]  # noqa: E501
        return self.tokenized_text_filtred

    def normalize(self, tokens: List[str] = []) -> List[str]:

        words_white = ["vc", "pv", 'fds', 'blz', 'tmj', 'pdc', 's2', 'sdds', 'sqn', 'mlr', 'tldg', 'tb', 'bj', 'obg', 'pfv', 'msg', 'add']  # noqa: E501
        words_black = ["none", "None"]
        words = [str(word).lower() for word in tokens if word is not None]  # noqa: E501
        self.normalized_text = []

        for word in words:
            correct_word = self.spell.correction(word)
            if word in words_white or correct_word in words_white:
                correct_word = word
            if word in words_black or correct_word in words_black:
                continue
            if word is None:
                continue
            if correct_word is None:
                correct_word = word
            self.normalized_text.append(str(correct_word))

        return self.normalized_text

    def lemmatization(self, tokens: List[str] = []) -> List[str]:
        doc = self.nlp(str([str(word) for word in tokens]))
        self.lemmarized_text = [token.lemma_ for token in doc if token.pos_ == 'NOUN']  # noqa: E501
        return self.lemmarized_text

    def stemming(self, tokens: List[str] = []) -> List[str]:
        self.stemmed_text = [self.stemmer.stem(str(word)) for word in tokens]  # noqa: E501
        return self.stemmed_text

    def digest(self, text: str = ""):
        text = self.text_cleaning(text)
        tokens = self.tokenize(text)
        tokens = self.removal_stop_word(tokens)
        tokens = self.normalize(tokens)
        lemma = self.lemmatization(tokens)
        stems = self.stemming(tokens)
        return {"tokens": tokens, "lemma": lemma, "stems": stems}  # noqa: E501
