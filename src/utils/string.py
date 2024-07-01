# flake8: noqa: E501

import re
import string
# import spacy
from typing import List
# from spellchecker import SpellChecker
from nltk.tokenize import word_tokenize

from src.utils.stop_words import stopwords_pt

def split_to_lines(content: str = "")-> List[str]:
    """quegra o conteúdo em linhas"""
    
    # Regex para identificar quebras de linha
    lines = re.split(r'\r?\n', content.strip())
    return [line.strip().encode('utf-8').decode('utf-8') for line in lines]

def split_to_phrases(content: str = "")-> List[str]:
    """transforms o conteúdo em freses"""
    
    # Regex para identificar pontos finais seguidos de um espaço ou fim da string
    phrases = re.split(r'(?<=\.)\s', content.strip())
    
    
    return [phrase.strip().encode('utf-8').decode('utf-8') for phrase in phrases]

def split_to_pargraphs(content: str = "") -> List[str]:
    """separa um texto em parágrafos"""
    
    paragraphs_split = re.split(r'(?:\r?\n){2,}', content.strip())
    paragraphs = []

    for paragraph in paragraphs_split:
        # Remove quebras de linha dentro dos parágrafos
        paragraph_unique = re.sub(r'\r?\n', ' ', paragraph).strip()
        paragraphs.append(paragraph_unique.encode('utf-8').decode('utf-8'))

    return paragraphs

def split_to_chunks(content: str = "", size: int = 1000)-> List[str]:
    """quebra o conteúdo em pedaços baseado em paragrafos"""
    
    paragraphs = split_to_pargraphs(content)
    chunks = []
    
    for paragraph in paragraphs:
        # transforma um parágrafo em chunks (pedaços de texto)
        cks = split_to_chunks_raw(paragraph.encode('utf-8').decode('utf-8'), size)
        chunks.extend(cks)
        
    return chunks

def split_to_chunks_raw(content: str = "", size: int = 1000) -> List[str]:
    """Quebra o texto em pedaços conforme definido"""
    
    # Regex para capturar chunks de tamanho específico
    pattern = re.compile(f'.{{1,{size}}}')
    return pattern.findall(content.encode('utf-8').decode('utf-8'))

def clean_lines(line: str = "") -> str:
    """Limpa uma linha com muitos espaços e saltos de \n"""
    
    line = re.sub(r' +|\n+', ' ', line.encode('utf-8').decode('utf-8')).strip()
    return line.strip(string.punctuation)

def clean(text: str = "") -> str:
    """limpa texto para processamento"""
    
    # Remover sinais de pontuação e caracteres não alfanuméricos. Isso remove tudo exceto letras, números e espaços
    text = re.sub(r'[^\w\s]', '', text)

    # Remover espaços extras
    clean_text = re.sub(r'\s+', ' ', text).strip()
    
    return clean_lines(clean_text)

def tokenize(text: str = "") -> List[str]:
    """ transfomaq o texto em tokens """
    tokens = word_tokenize(text)
    return [str(token) for token in tokens if token.isalpha()]

def normalize(text: str = "") -> List[str]:
    """ normaliza o texto corriginjo palavra com grafia errada """

    # words_white = ["vc", "pv", 'fds', 'blz', 'tmj', 'pdc', 's2', 'sdds', 'sqn', 'mlr', 'tldg', 'tb', 'bj', 'obg', 'pfv', 'msg', 'add']
    # words_black = ["none", "None"]
    # words = [str(word).lower() for word in tokenize(text) if word is not None]
    # normalized_text = []
    # spell = SpellChecker(language='pt')

    # for word in words:
    #     correct_word = spell.correction(word)
    #     if word in words_white or correct_word in words_white:
    #         correct_word = word
    #     if word in words_black or correct_word in words_black:
    #         continue
    #     if word is None:
    #         continue
    #     if correct_word is None:
    #         correct_word = word
    #     normalized_text.append(str(correct_word))

    # return normalized_text
    return []

def lemmatization(text: str = "") ->  List[str]:
    # nlp = spacy.load('pt_core_news_sm')
    # doc = nlp(str([str(word) for word in tokenize(text)]))
    # return [token.lemma_ for token in doc if token.pos_ == 'NOUN']
    return []

def removal_stopwords(text: str = "") -> str:
    """ Remove as plavras de parada a lista """
    # Tokenização
    tokens = tokenize(text)
    
    # Remover pontuação
    tokens = [clean_lines(word) for word in tokens]
    
    # Remover stopwords
    tokens = [word for word in tokens if word.lower() not in stopwords_pt]
    
    return ' '.join(tokens)

def unique(contents: List[str] = []) -> List[str]:
    """ remove documentos com conteúdo repetido """
    content_unique = set()
    results: List[str] = []
    for content in contents:
        if content not in content_unique:
            results.append(content)
            content_unique.add(content)
    return results