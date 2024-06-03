# flake8: noqa: E501

import string
from sklearn.feature_extraction.text import CountVectorizer

stopwords_pt = [
    "a", "à", "ao", "aos", "as", "às", "de", "do", "da", "dos", "das", "em", "no", "na", "nos", "nas",
    "por", "pelos", "pela", "pelas", "o", "os", "um", "uns", "uma", "umas", "e", "é", "que", "com",
    "se", "não", "para", "como", "mais", "mas", "ou", "quando", "muito", "já", "era", "são", "seu",
    "sua", "seus", "suas", "me", "minha", "meu", "meus", "minhas", "este", "estes", "esta", "estas",
    "esse", "esses", "essa", "essas", "isto", "isso", "aquilo", "aquele", "aquela", "aqueles",
    "aquelas", "um", "uma", "uns", "umas", "ele", "ela", "eles", "elas", "nos", "lhe", "lhes"
]

def process_text(text):
    # Tokenização
    tokens = text.split()
    
    # Remover pontuação
    tokens = [word.strip(string.punctuation) for word in tokens]
    
    # Remover stopwords
    tokens = [word for word in tokens if word.lower() not in stopwords_pt]
    
    return ' '.join(tokens)


def generate_bow(text: str = ""):
    processed_corpus = process_text(text)
    # Gerar Bag of Words
    vectorizer = CountVectorizer()
    bow = vectorizer.fit_transform([processed_corpus])
    
    return [item for b in bow.toarray() for item in b], vectorizer.get_feature_names_out()