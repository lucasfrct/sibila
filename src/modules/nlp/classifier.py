

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

from joblib import dump, load


def classifier_save(path, model, vectorizer):  # noqa: E501
    # Salvar o modelo e o vetorizador
    dump(model, f"{path}.model.joblib")
    dump(vectorizer, f"{path}.vectorizer.tfidf.joblib")


def classifier_load(path):
    # Carregar o modelo e o vetorizador
    model = load(f"{path}.model.joblib")
    vectorizer = load(f"{path}.vectorizer.tfidf.joblib")
    return model, vectorizer


def classifier(text: str = ""):
    # Novo texto para previsão
    texts = [text]

    model, vectorizer = classifier_load("./a1")
    text_matrix = vectorizer.transform(texts)
    predicao = model.predict(text_matrix)
    return predicao


def classifier_train(intentions=[], texts=[]):

    # Dados de exemplo
    texts = [
        "Qual é o clima hoje?",
        "Quero reservar um voo para Paris.",
        "Preciso de uma receita de bolo de chocolate.",
        "Como está o tempo em Tokyo?",
        "Gostaria de um voo para Nova York amanhã.",
        "Como fazer brownie?"
    ]
    
    intentions = [
        "Obter_Clima",
        "Reservar_Voo",
        "Buscar_Receita",
        "Obter_Clima",
        "Reservar_Voo",
        "Buscar_Receita"
    ]

    # Vetorização dos textos
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)

    # Divisão dos dados em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, intentions, test_size=0.25, random_state=42)   # noqa: E501

    # Treinamento do modelo de Regressão Logística
    model = LogisticRegression()
    model.fit(X_train, y_train)
    
    classifier_save("./a1", model, vectorizer)

    # Avaliação do modelo
    predictions = model.predict(X_test)
    print(classification_report(y_test, predictions))
