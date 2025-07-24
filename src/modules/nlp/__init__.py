# Módulo NLP - Processamento de Linguagem Natural para Documentos Legais
# Agora com integração CrewAI para análise baseada em agentes

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

# Import CrewAI integration
try:
    from .crewai_integration import (
        CrewAINLPConfiguration, CrewAINLPAgents, CrewAINLPWorkflows,
        create_nlp_crew, analyze_text_with_crewai,
        crewai_sentiment_analysis, crewai_legal_classification,
        enhanced_sentiment_analysis_tool, legal_document_classification_tool,
        comprehensive_legal_analysis_tool, text_preprocessing_tool
    )
    from .crewai_pipeline import (
        CrewAIPipelineManager, create_pipeline_manager,
        execute_legal_document_pipeline, execute_batch_processing_pipeline,
        get_available_pipelines
    )
    from .crewai_config import CrewAINLPConfig, validate_environment, get_configuration_summary
    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False

# Import enhanced sentiment analysis
try:
    from .enhanced_sentiment import (
        EnhancedSentimentAnalyzer, SentimentFilter,
        sentiment_analysis_enhanced, sentiment_classification_only
    )
    ENHANCED_SENTIMENT_AVAILABLE = True
except ImportError:
    ENHANCED_SENTIMENT_AVAILABLE = False

__all__ = [
    'classifier', 'classifier_train', 'classifier_save', 'classifier_load',
    'classify_subject', 'classify_article_type', 'classify_legal_intention',
    'generate_title', 'classify_legal_category', 'classify_normative_type',
    'classify_document', 'SimpleLegalClassifier', 'get_simple_classifier'
]

if ENHANCED_AVAILABLE:
    __all__.extend(['LegalDocumentClassifier', 'ClassificationType', 'get_classifier'])

if ENHANCED_SENTIMENT_AVAILABLE:
    __all__.extend([
        'EnhancedSentimentAnalyzer', 'SentimentFilter',
        'sentiment_analysis_enhanced', 'sentiment_classification_only'
    ])

if CREWAI_AVAILABLE:
    __all__.extend([
        'CrewAINLPConfiguration', 'CrewAINLPAgents', 'CrewAINLPWorkflows',
        'create_nlp_crew', 'analyze_text_with_crewai',
        'crewai_sentiment_analysis', 'crewai_legal_classification',
        'enhanced_sentiment_analysis_tool', 'legal_document_classification_tool',
        'comprehensive_legal_analysis_tool', 'text_preprocessing_tool',
        'CrewAIPipelineManager', 'create_pipeline_manager',
        'execute_legal_document_pipeline', 'execute_batch_processing_pipeline',
        'get_available_pipelines', 'CrewAINLPConfig', 'validate_environment',
        'get_configuration_summary'
    ])