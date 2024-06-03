# flake8: noqa: E501

from sklearn.feature_extraction.text import CountVectorizer

from src.utils import string as Str

def generate_bow(text: str = "")-> dict:
    """Gerar Bag of Words"""
    
    processed_text = Str.removal_stopwords(text)
    vectorizer = CountVectorizer()
    bow = vectorizer.fit_transform([processed_text])
    
    freq = [item for b in bow.toarray() for item in b]
    words = [item for item in vectorizer.get_feature_names_out()]
    
    vocabulary: dict = {}
    for word, weight in zip(words, freq):
        vocabulary[word] = weight
    
    return vocabulary