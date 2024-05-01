import re
import unidecode

from typing import List

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


class PreProcessor:
    def __init__(self, text: str = ""):
        
        nltk.download('stopwords')
        self.stop_words = set(stopwords.words('portuguese'))

        self.text = text

        self.tokenized_text_filtred: List[str] = []
        self.tokenized_text: List[str] = []
        self.normalized_text = ""
        self.stemmed_text = ""
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
        self.tokenized_text = [token for token in tokens if token.isalpha()]  # noqa: E501
        return self.tokenized_text

    def removal_stop_word(self, tokens: List[str] = []) -> List[str]:
        self.tokenized_text_filtred = [word for word in tokens if word not in self.stop_words]  # noqa: E501
        return self.tokenized_text_filtred

    def normalize(self, tokens: List[str] = []):
        self.normalized_text = [re.sub(r'\s+', '', word.lower().strip()) for word in tokens]  # noqa: E501
        return self.normalized_text

    def lemmatization(self, text: str = ""):
        return self.stemmed_text
