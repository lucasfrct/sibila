from textblob import TextBlob
from textblob import Word


def sentiment_analysis(text: str = "") -> str:

    if text == "":
        return None

    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0:
        return "Positive"

    if polarity < 0:
        return "Negative"

    return "Neutral"


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
