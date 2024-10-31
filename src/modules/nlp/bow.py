# flake8: noqa: E501

from sklearn.feature_extraction.text import CountVectorizer

from src.utils import string as Str

def generate_bow(content: str = "")-> dict:
    """Gerar Bag of Words"""
    
    processed_content = Str.removal_stopwords(content)
    vectorizer = CountVectorizer()
    bow = vectorizer.fit_transform([processed_content])
    
    freq = [item for b in bow.toarray() for item in b]
    words = [item for item in vectorizer.get_feature_names_out()]
    
    vocabulary: dict = {}
    for word, weight in zip(words, freq):
        vocabulary[word] = weight
    
    return vocabulary


def relevant_words(content: str = "", cut: int = 3) -> str:
    """
    Relevante Words: retorna apenas as palavra relevantes num texto

    Args:
        content (str): Conteúdo de origem.
        cut (int): corte inferior da frequência das palavras selecionadas.

    Returns:
        str: retorna um texto com as palavras relevantes separadas por espaço.
    """
    bow = generate_bow(content)
    main_words = []
    for word in bow.keys():
        freq = bow[word]
        if(freq >= cut):
            main_words.append(word)
            
    return ' '.join(main_words)