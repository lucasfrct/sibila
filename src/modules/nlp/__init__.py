# Módulo NLP - Processamento de Linguagem Natural para Documentos Legais

from .classifier import (
    classifier, classifier_train, classifier_save, classifier_load,
    classify_subject, classify_article_type, classify_legal_intention,
    generate_title, classify_legal_category, classify_normative_type,
    classify_document
)

from .simple_classifier import SimpleLegalClassifier, get_simple_classifier

try:
    from .enhanced_classifier import LegalDocumentClassifier, ClassificationType, get_classifier
    ENHANCED_AVAILABLE = True
except ImportError:
    ENHANCED_AVAILABLE = False

__all__ = [
    'classifier', 'classifier_train', 'classifier_save', 'classifier_load',
    'classify_subject', 'classify_article_type', 'classify_legal_intention',
    'generate_title', 'classify_legal_category', 'classify_normative_type',
    'classify_document', 'SimpleLegalClassifier', 'get_simple_classifier'
]

if ENHANCED_AVAILABLE:
    __all__.extend(['LegalDocumentClassifier', 'ClassificationType', 'get_classifier'])