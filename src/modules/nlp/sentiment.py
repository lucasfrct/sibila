
"""
Módulo de análise de sentimento utilizando TextBlob.

Este módulo fornece funcionalidades básicas para análise de sentimento
e processamento de texto natural.
"""
from textblob import TextBlob
from textblob import Word
from .enhanced_sentiment import EnhancedSentimentAnalyzer, SentimentFilter, sentiment_analysis_enhanced, sentiment_classification_only



def sentiment_analysis(text: str = "") -> str:
    """
    Analisa o sentimento de um texto.
    
    Args:
        text (str): O texto para análise de sentimento.
        
    Returns:
        str: Classificação do sentimento ("Positivo", "Negativo", "Neutro") ou None se texto vazio.
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
        text (str): O texto para análise.
        
    Returns:
        list: Lista de tags ou None se texto vazio.
    """

    if text == "":
        return None

    blob = TextBlob(text)
    return blob.tags


def sentiment_noun_phrases(text: str = ""):
    """
    Extrai as frases nominais de um texto.
    
    Args:
        text (str): O texto para análise.
        
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
        text (str): O texto para divisão.
        
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
        text (str): O texto para análise.
        
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
        text (str): O texto para singularização.
        
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
        text (str): O texto para pluralização.
        
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

    Basic sentiment analysis (backward compatibility)
    For enhanced analysis, use sentiment_analysis_enhanced()
    """
    if text == "":
        return None

    return sentiment_classification_only(text)


def sentiment_analysis_comprehensive(text: str = "") -> dict:
    """
    Comprehensive sentiment analysis with multiple dimensions
    Returns detailed analysis including emotions, intensity, aspects, etc.
    """
    if text == "":
        return None
    
    return sentiment_analysis_enhanced(text)


def sentiment_tags(text: str = ""):

    if text == "":
        return None

    blob = TextBlob(text)
    return blob.tags


def sentiment_noun_phrases(text: str = ""):

    if text == "":
        return None

    blob = TextBlob(text)
    return blob.noun_phrases


def sentiment_sentenses(text: str = ""):

    if text == "":
        return None

    blob = TextBlob(text)
    return blob.sentences


def sentiment_words(text: str = ""):

    if text == "":
        return None

    blob = TextBlob(text)
    return blob.words


def sentiment_words_sigularize(text: str = ""):

    if text == "":
        return None

    blob = TextBlob(text)

    words = []
    for word in blob.words:
        words.append(word.singularize())
    return words


def sentiment_words_pluralize(text: str = ""):

    if text == "":
        return None

    blob = TextBlob(text)

    words = []
    for word in blob.words:
        words.append(word.pluralize())
    return words


def sentiment_lemmarize(text: str = ""):
    w = Word(text)
    return w.lemmatize()


def sentiment_verb(text: str = ""):
    w = Word(text)
    return w.lemmatize("v")
