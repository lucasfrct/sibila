# CrewAI NLP Configuration
# Default configuration for CrewAI NLP agents and workflows

import os
from typing import Dict, Any


class CrewAINLPConfig:
    """Configuration class for CrewAI NLP integration"""
    
    # Default LLM configuration
    DEFAULT_LLM_CONFIG = {
        "model": "gpt-3.5-turbo",
        "temperature": 0.1,
        "max_tokens": 1500,
        "timeout": 60
    }
    
    # Environment-based LLM configuration
    @classmethod
    def get_llm_config(cls) -> Dict[str, Any]:
        """Get LLM configuration from environment or defaults"""
        return {
            "model": os.getenv("CREWAI_MODEL", cls.DEFAULT_LLM_CONFIG["model"]),
            "temperature": float(os.getenv("CREWAI_TEMPERATURE", cls.DEFAULT_LLM_CONFIG["temperature"])),
            "max_tokens": int(os.getenv("CREWAI_MAX_TOKENS", cls.DEFAULT_LLM_CONFIG["max_tokens"])),
            "timeout": int(os.getenv("CREWAI_TIMEOUT", cls.DEFAULT_LLM_CONFIG["timeout"]))
        }
    
    # Agent role definitions in Portuguese for legal domain
    AGENT_ROLES = {
        "sentiment_analyst": {
            "role": "Analista de Sentimentos Legal",
            "goal": "Analisar sentimentos e emoções em textos legais e documentos oficiais com precisão e contextualização jurídica",
            "backstory": """Você é um especialista em análise de sentimentos com formação em direito e linguística computacional. 
            Possui vasta experiência em interpretar nuances emocionais em textos formais, contratos, petições e documentos legais. 
            Sua expertise inclui detecção de tom argumentativo, análise de subjetividade em pareceres jurídicos e identificação 
            de sentimentos implícitos em documentos normativos.""",
            "verbose": True,
            "allow_delegation": False
        },
        
        "legal_classifier": {
            "role": "Classificador Jurídico Especializado",
            "goal": "Classificar documentos legais por área do direito, tipo normativo, hierarquia legal e propósito jurídico",
            "backstory": """Você é um jurista especializado em taxonomia legal e classificação de documentos jurídicos. 
            Com profundo conhecimento do ordenamento jurídico brasileiro, você é capaz de identificar a natureza legal de documentos, 
            classificá-los por ramos do direito, determinar sua hierarquia normativa e identificar sua finalidade específica. 
            Sua expertise abrange desde leis constitucionais até atos administrativos e contratos privados.""",
            "verbose": True,
            "allow_delegation": False
        },
        
        "text_analyzer": {
            "role": "Analista Textual Avançado",
            "goal": "Realizar análise estrutural e semântica profunda de textos legais e documentos especializados",
            "backstory": """Você é um especialista em linguística computacional com foco em análise de textos jurídicos. 
            Domina técnicas avançadas de processamento de linguagem natural, extração de entidades, análise sintática e semântica. 
            Sua expertise inclui identificação de padrões textuais, estruturação de conteúdo legal e análise de coesão textual 
            em documentos formais e técnicos.""",
            "verbose": True,
            "allow_delegation": False
        },
        
        "legal_researcher": {
            "role": "Pesquisador Jurídico Inteligente",
            "goal": "Realizar pesquisa e análise contextual de documentos legais, identificando precedentes e conexões jurídicas",
            "backstory": """Você é um pesquisador jurídico com vasta experiência em análise documental e pesquisa legal. 
            Especializa-se em identificar conexões entre diferentes normas, localizar precedentes relevantes e contextualizar 
            documentos dentro do sistema jurídico brasileiro. Sua expertise inclui análise de jurisprudência, doutrina e 
            interpretação sistemática de normas.""",
            "verbose": True,
            "allow_delegation": False
        }
    }
    
    # Workflow configurations
    WORKFLOW_CONFIGS = {
        "sentiment_analysis": {
            "name": "Análise de Sentimentos Legal",
            "description": "Workflow especializado em análise de sentimentos para documentos legais",
            "agents": ["sentiment_analyst", "text_analyzer"],
            "complexity": "medium"
        },
        
        "legal_classification": {
            "name": "Classificação de Documentos Legais",
            "description": "Workflow para classificação abrangente de documentos jurídicos",
            "agents": ["legal_classifier", "text_analyzer"],
            "complexity": "high"
        },
        
        "comprehensive_analysis": {
            "name": "Análise Legal Abrangente",
            "description": "Workflow completo combinando múltiplas análises especializadas",
            "agents": ["sentiment_analyst", "legal_classifier", "text_analyzer", "legal_researcher"],
            "complexity": "very_high"
        },
        
        "document_processing": {
            "name": "Processamento Inteligente de Documentos",
            "description": "Pipeline otimizado para processamento em lote de documentos legais",
            "agents": ["text_analyzer", "legal_classifier"],
            "complexity": "medium"
        }
    }
    
    # Tool configurations
    TOOL_CONFIGS = {
        "sentiment_tools": [
            "enhanced_sentiment_analysis_tool",
            "text_preprocessing_tool"
        ],
        
        "classification_tools": [
            "legal_document_classification_tool",
            "comprehensive_legal_analysis_tool",
            "text_preprocessing_tool"
        ],
        
        "analysis_tools": [
            "enhanced_sentiment_analysis_tool",
            "comprehensive_legal_analysis_tool",
            "text_preprocessing_tool"
        ],
        
        "file_tools": [
            "FileReadTool",
            "FileWriterTool"
        ]
    }
    
    # Performance and resource settings
    PERFORMANCE_CONFIG = {
        "max_concurrent_tasks": 3,
        "task_timeout": 300,  # 5 minutes
        "memory_limit": "1GB",
        "cache_enabled": True,
        "cache_ttl": 3600  # 1 hour
    }
    
    # Error handling and retry configuration
    ERROR_CONFIG = {
        "max_retries": 3,
        "retry_delay": 5,  # seconds
        "fallback_enabled": True,
        "log_errors": True
    }
    
    # Output formatting preferences
    OUTPUT_CONFIG = {
        "format": "json",
        "include_metadata": True,
        "include_confidence_scores": True,
        "locale": "pt_BR",
        "datetime_format": "%Y-%m-%d %H:%M:%S"
    }


# Environment variable mapping for easy configuration
ENVIRONMENT_MAPPING = {
    "OPENAI_API_KEY": "OpenAI API key for LLM access",
    "CREWAI_MODEL": "Default model for CrewAI agents",
    "CREWAI_TEMPERATURE": "Temperature setting for LLM responses",
    "CREWAI_MAX_TOKENS": "Maximum tokens for LLM responses",
    "CREWAI_TIMEOUT": "Timeout for LLM requests",
    "CREWAI_VERBOSE": "Enable verbose logging for CrewAI",
    "CREWAI_CACHE_ENABLED": "Enable caching for CrewAI responses",
    "CREWAI_MAX_RETRIES": "Maximum retries for failed operations"
}


def validate_environment() -> Dict[str, bool]:
    """Validate required environment variables and configurations"""
    validation_results = {}
    
    # Check for OpenAI API key (required for most LLMs)
    validation_results["openai_api_key"] = bool(os.getenv("OPENAI_API_KEY"))
    
    # Check CrewAI installation
    try:
        import crewai
        validation_results["crewai_installed"] = True
    except ImportError:
        validation_results["crewai_installed"] = False
    
    # Check CrewAI tools installation
    try:
        import crewai_tools
        validation_results["crewai_tools_installed"] = True
    except ImportError:
        validation_results["crewai_tools_installed"] = False
    
    # Check required NLP dependencies
    required_packages = ["textblob", "vaderSentiment", "nltk", "sklearn"]
    for package in required_packages:
        try:
            __import__(package)
            validation_results[f"{package}_available"] = True
        except ImportError:
            validation_results[f"{package}_available"] = False
    
    return validation_results


def get_configuration_summary() -> Dict[str, Any]:
    """Get summary of current CrewAI NLP configuration"""
    return {
        "llm_config": CrewAINLPConfig.get_llm_config(),
        "available_agents": list(CrewAINLPConfig.AGENT_ROLES.keys()),
        "available_workflows": list(CrewAINLPConfig.WORKFLOW_CONFIGS.keys()),
        "environment_validation": validate_environment(),
        "performance_settings": CrewAINLPConfig.PERFORMANCE_CONFIG,
        "output_settings": CrewAINLPConfig.OUTPUT_CONFIG
    }