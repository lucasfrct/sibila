"""
Módulo de análise de sentimento em português.

Este módulo fornece funcionalidades para análise de sentimento de textos em português,
incluindo classificação de polaridade, extração de tags, frases nominais, sentenças,
palavras e operações de lematização.
"""

from textblob import TextBlob
from textblob import Word


def sentiment_analysis(text: str = "") -> str:
    """
    Analisa o sentimento de um texto e retorna a classificação em português.
    
    Args:
        text (str): O texto para análise de sentimento. Padrão é string vazia.
        
    Returns:
        str: Classificação do sentimento ("Positivo", "Negativo", "Neutro") ou None se texto vazio.
        
    Example:
        >>> sentiment_analysis("Eu amo este produto!")
        "Positivo"
        >>> sentiment_analysis("Este produto é terrível")
        "Negativo"
    """
    if text == "":
        return None

    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0:
        return "Positivo"

    if polarity < 0:
        return "Negativo"

    return "Neutro"


def sentiment_tags(text: str = ""):
    """
    Extrai as tags de partes do discurso de um texto.
    
    Args:
        text (str): O texto para extração de tags. Padrão é string vazia.
        
    Returns:
        list: Lista de tags de partes do discurso ou None se texto vazio.
    """
    if text == "":
        return None

    blob = TextBlob(text)
    return blob.tags


def sentiment_noun_phrases(text: str = ""):
    """
    Extrai as frases nominais de um texto.
    
    Args:
        text (str): O texto para extração de frases nominais. Padrão é string vazia.
        
    Returns:
        list: Lista de frases nominais ou None se texto vazio.
    """
    if text == "":
        return None

    blob = TextBlob(text)
    return blob.noun_phrases


def sentiment_sentenses(text: str = ""):
    """
    Divide o texto em sentenças.
    
    Args:
        text (str): O texto para divisão em sentenças. Padrão é string vazia.
        
    Returns:
        list: Lista de sentenças ou None se texto vazio.
    """
    if text == "":
        return None

    blob = TextBlob(text)
    return blob.sentences


def sentiment_words(text: str = ""):
    """
    Extrai as palavras de um texto.
    
    Args:
        text (str): O texto para extração de palavras. Padrão é string vazia.
        
    Returns:
        list: Lista de palavras ou None se texto vazio.
    """
    if text == "":
        return None

    blob = TextBlob(text)
    return blob.words


def sentiment_words_sigularize(text: str = ""):
    """
    Singulariza todas as palavras de um texto.
    
    Args:
        text (str): O texto para singularização das palavras. Padrão é string vazia.
        
    Returns:
        list: Lista de palavras singularizadas ou None se texto vazio.
    """
    if text == "":
        return None

    blob = TextBlob(text)

    words = []
    for word in blob.words:
        words.append(word.singularize())
    return words


def sentiment_words_pluralize(text: str = ""):
    """
    Pluraliza todas as palavras de um texto.
    
    Args:
        text (str): O texto para pluralização das palavras. Padrão é string vazia.
        
    Returns:
        list: Lista de palavras pluralizadas ou None se texto vazio.
    """
    if text == "":
        return None

    blob = TextBlob(text)

    words = []
    for word in blob.words:
        words.append(word.pluralize())
    return words


def sentiment_lemmarize(text: str = ""):
    """
    Lematiza uma palavra (reduz à sua forma base).
    
    Args:
        text (str): A palavra para lematização.
        
    Returns:
        str: Palavra lematizada.
    """
    w = Word(text)
    return w.lemmatize()


def sentiment_verb(text: str = ""):
    """
    Lematiza uma palavra como verbo.
    
    Args:
        text (str): A palavra para lematização como verbo.
        
    Returns:
        str: Verbo lematizado.
    """
    w = Word(text)
    return w.lemmatize("v")