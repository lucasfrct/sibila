from textblob import TextBlob
from textblob import Word
from .enhanced_sentiment import EnhancedSentimentAnalyzer, SentimentFilter, sentiment_analysis_enhanced, sentiment_classification_only


def sentiment_analysis(text: str = "") -> str:
    """
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
