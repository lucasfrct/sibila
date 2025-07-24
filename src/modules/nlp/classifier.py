# flake8: noqa: E501

import logging

# Try importing sklearn-based components
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import classification_report
    from joblib import dump, load
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

# Import the enhanced classifier
try:
    from src.modules.nlp.enhanced_classifier import get_classifier, LegalDocumentClassifier, ClassificationType
    ENHANCED_AVAILABLE = True
except ImportError:
    ENHANCED_AVAILABLE = False

# Import the simple classifier as fallback
try:
    from src.modules.nlp.simple_classifier import get_simple_classifier, SimpleLegalClassifier
    SIMPLE_AVAILABLE = True
except ImportError:
    SIMPLE_AVAILABLE = False


def classifier_save(path, model, vectorizer):  # noqa: E501
    """Salvar o modelo e o vetorizador (função legacy)"""
    if SKLEARN_AVAILABLE:
        dump(model, f"{path}.model.joblib")
        dump(vectorizer, f"{path}.vectorizer.tfidf.joblib")
    else:
        logging.warning("sklearn não disponível. Não é possível salvar modelos.")


def classifier_load(path):
    """Carregar o modelo e o vetorizador (função legacy)"""
    if SKLEARN_AVAILABLE:
        model = load(f"{path}.model.joblib")
        vectorizer = load(f"{path}.vectorizer.tfidf.joblib")
        return model, vectorizer
    else:
        logging.warning("sklearn não disponível. Não é possível carregar modelos.")
        return None, None


def classifier(text: str = ""):
    """
    Classificação de texto usando o novo classificador aprimorado
    Mantém compatibilidade com a API antiga
    """
    if ENHANCED_AVAILABLE:
        legal_classifier = get_classifier()
        result = legal_classifier.classify_subject(text)
        return [result] if result else ["Indefinido"]
    elif SIMPLE_AVAILABLE:
        simple_classifier = get_simple_classifier()
        result = simple_classifier.classify_subject(text)
        return [result] if result else ["Indefinido"]
    else:
        # Fallback para método antigo se disponível
        if SKLEARN_AVAILABLE:
            try:
                texts = [text]
                model, vectorizer = classifier_load("./a1")
                if model and vectorizer:
                    text_matrix = vectorizer.transform(texts)
                    predicao = model.predict(text_matrix)
                    return predicao
            except Exception as e:
                logging.error(f"Erro na classificação: {e}")
        
        return ["Indefinido"]


def classifier_train(intentions=[], texts=[]):
    """
    Treinamento do classificador usando o novo sistema aprimorado
    Mantém compatibilidade com a API antiga
    """
    if ENHANCED_AVAILABLE:
        legal_classifier = get_classifier()
        
        if texts and intentions:
            # Usar dados fornecidos
            legal_classifier.train_classifier(ClassificationType.SUBJECT, texts, intentions)
        else:
            # Treinar todos os classificadores com dados padrão
            legal_classifier.train_all_classifiers()
        
        logging.info("Treinamento do classificador aprimorado concluído")
    elif SIMPLE_AVAILABLE:
        logging.info("Usando classificador baseado em padrões (não requer treinamento)")
    elif SKLEARN_AVAILABLE:
        # Fallback para método antigo
        if not texts or not intentions:
            # Dados de exemplo padrão
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
    else:
        logging.warning("Nenhum método de treinamento disponível")


# Novas funções para usar as funcionalidades aprimoradas
def classify_document(document_path: str):
    """
    Classifica um documento completo usando o classificador aprimorado
    """
    if ENHANCED_AVAILABLE:
        legal_classifier = get_classifier()
        return legal_classifier.analyze_document_content(document_path)
    elif SIMPLE_AVAILABLE:
        simple_classifier = get_simple_classifier()
        return simple_classifier.analyze_document_content(document_path)
    else:
        logging.warning("Classificador aprimorado não disponível")
        return {}


def classify_subject(text: str):
    """Classifica o assunto de um texto"""
    if ENHANCED_AVAILABLE:
        legal_classifier = get_classifier()
        return legal_classifier.classify_subject(text)
    elif SIMPLE_AVAILABLE:
        simple_classifier = get_simple_classifier()
        return simple_classifier.classify_subject(text)
    else:
        result = classifier(text)
        return result[0] if result else "Indefinido"


def classify_article_type(text: str):
    """Classifica o tipo de artigo"""
    if ENHANCED_AVAILABLE:
        legal_classifier = get_classifier()
        return legal_classifier.classify_article_type(text)
    elif SIMPLE_AVAILABLE:
        simple_classifier = get_simple_classifier()
        return simple_classifier.classify_article_type(text)
    else:
        logging.warning("Classificação de tipo de artigo não disponível no modo legacy")
        return "Indefinido"


def classify_legal_intention(text: str):
    """Classifica a intenção legal"""
    if ENHANCED_AVAILABLE:
        legal_classifier = get_classifier()
        return legal_classifier.classify_legal_intention(text)
    elif SIMPLE_AVAILABLE:
        simple_classifier = get_simple_classifier()
        return simple_classifier.classify_legal_intention(text)
    else:
        logging.warning("Classificação de intenção legal não disponível no modo legacy")
        return "Indefinido"


def generate_title(text: str):
    """Gera um título para o texto"""
    if ENHANCED_AVAILABLE:
        legal_classifier = get_classifier()
        return legal_classifier.generate_title(text)
    elif SIMPLE_AVAILABLE:
        simple_classifier = get_simple_classifier()
        return simple_classifier.generate_title(text)
    else:
        logging.warning("Geração de título não disponível no modo legacy")
        return "Título Indefinido"


def classify_legal_category(text: str):
    """Classifica a categoria legal"""
    if ENHANCED_AVAILABLE:
        legal_classifier = get_classifier()
        return legal_classifier.classify_legal_category(text)
    elif SIMPLE_AVAILABLE:
        simple_classifier = get_simple_classifier()
        return simple_classifier.classify_legal_category(text)
    else:
        logging.warning("Classificação de categoria legal não disponível no modo legacy")
        return "Categoria Indefinida"


def classify_normative_type(text: str):
    """Classifica o tipo normativo"""
    if ENHANCED_AVAILABLE:
        legal_classifier = get_classifier()
        return legal_classifier.classify_normative_type(text)
    elif SIMPLE_AVAILABLE:
        simple_classifier = get_simple_classifier()
        return simple_classifier.classify_normative_type(text)
    else:
        logging.warning("Classificação de tipo normativo não disponível no modo legacy")
        return "Tipo Indefinido"