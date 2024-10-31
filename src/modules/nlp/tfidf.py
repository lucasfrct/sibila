# flake8: noqa: E501

from sklearn.feature_extraction.text import TfidfVectorizer

def generate_tfidf(text: str = "") -> dict:
    """ matrix de características TF-IDF(Term Frequency-Inverse Document Frequency)""" 
    
    tfidf_vectorizer = TfidfVectorizer()

    # Transformação dos documentos em uma matriz TF-IDF
    tfidf = tfidf_vectorizer.fit_transform([text])
    tfidf_matrix = tfidf.toarray()

    # Vocabulário com índices
    vocabulary_tfidf_list = tfidf_vectorizer.get_feature_names_out()

    # Monta um vocabulario de frequencia
    vocabulary = {}
    for word, weight in zip(vocabulary_tfidf_list, tfidf_matrix[0]):
        vocabulary[word] = weight

    return vocabulary