# CrewAI Integration Module for NLP
# Provides agent-based natural language processing using CrewAI framework

import logging
import json
from typing import Dict, List, Optional, Any

# Conditional imports for CrewAI
try:
    from crewai import Agent, Task, Crew
    from crewai.tools import tool
    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False
    # Create dummy classes for type hints
    class Agent:
        pass
    class Task:
        pass
    class Crew:
        pass
    def tool(name):
        def decorator(func):
            return func
        return decorator

try:
    from crewai_tools import FileReadTool, FileWriterTool
    CREWAI_TOOLS_AVAILABLE = True
except ImportError:
    CREWAI_TOOLS_AVAILABLE = False
    class FileReadTool:
        pass
    class FileWriterTool:
        pass

# Import existing NLP modules for backward compatibility
try:
    from .enhanced_sentiment import EnhancedSentimentAnalyzer, sentiment_analysis_enhanced
    ENHANCED_SENTIMENT_AVAILABLE = True
except ImportError:
    ENHANCED_SENTIMENT_AVAILABLE = False
    logging.warning("Enhanced sentiment analysis not available")

try:
    from .enhanced_classifier import LegalDocumentClassifier, ClassificationType, get_classifier
    ENHANCED_CLASSIFIER_AVAILABLE = True
except ImportError:
    ENHANCED_CLASSIFIER_AVAILABLE = False
    logging.warning("Enhanced classifier not available")


class CrewAINLPConfiguration:
    """Configuration class for CrewAI NLP agents and workflows"""
    
    def __init__(self):
        self.llm_config = {
            "model": "gpt-3.5-turbo",  # Default model, can be overridden
            "temperature": 0.1,
            "max_tokens": 1000
        }
        
        # Agent configurations
        self.sentiment_agent_config = {
            "role": "Analista de Sentimentos",
            "goal": "Analisar sentimentos em textos legais e documentos, fornecendo análises abrangentes e precisas",
            "backstory": "Você é um especialista em análise de sentimentos com foco em documentos legais e textos formais. Sua expertise inclui detecção de emoções, análise de subjetividade e sentimentos baseados em aspectos.",
            "verbose": True,
            "allow_delegation": False
        }
        
        self.legal_classifier_agent_config = {
            "role": "Classificador de Documentos Legais",
            "goal": "Classificar documentos legais por assunto, tipo, categoria e intenção legal com alta precisão",
            "backstory": "Você é um especialista em direito e classificação de documentos legais. Possui vasto conhecimento sobre diferentes tipos de normativos, categorias legais e estruturas jurídicas brasileiras.",
            "verbose": True,
            "allow_delegation": False
        }
        
        self.text_analyzer_agent_config = {
            "role": "Analisador de Texto Avançado",
            "goal": "Realizar análises textuais avançadas incluindo extração de entidades, identificação de padrões e análise estrutural",
            "backstory": "Você é um especialista em processamento de linguagem natural com foco em análise textual profunda. Sua expertise inclui extração de informações, análise sintática e semântica.",
            "verbose": True,
            "allow_delegation": False
        }


@tool("Enhanced Sentiment Analysis Tool")
def enhanced_sentiment_analysis_tool(text: str) -> str:
    """
    Ferramenta para análise de sentimentos abrangente usando o EnhancedSentimentAnalyzer.
    
    Args:
        text: Texto para análise de sentimentos
        
    Returns:
        JSON string com análise completa de sentimentos
    """
    if not ENHANCED_SENTIMENT_AVAILABLE:
        return json.dumps({
            "error": "Enhanced sentiment analysis not available",
            "message": "Required dependencies not installed"
        }, ensure_ascii=False)
    
    try:
        analyzer = EnhancedSentimentAnalyzer()
        result = analyzer.analyze_comprehensive(text)
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Erro na análise de sentimentos: {str(e)}"}, ensure_ascii=False)


@tool("Legal Document Classification Tool")  
def legal_document_classification_tool(text: str, classification_type: str = "subject") -> str:
    """
    Ferramenta para classificação de documentos legais usando o LegalDocumentClassifier.
    
    Args:
        text: Texto do documento legal para classificação
        classification_type: Tipo de classificação (subject, article_type, legal_intention, etc.)
        
    Returns:
        JSON string com resultado da classificação
    """
    if not ENHANCED_CLASSIFIER_AVAILABLE:
        return json.dumps({
            "error": "Enhanced classifier not available",
            "message": "Required dependencies not installed"
        }, ensure_ascii=False)
    
    try:
        classifier = get_classifier()
        
        # Map string to enum
        type_mapping = {
            "subject": ClassificationType.SUBJECT,
            "article_type": ClassificationType.ARTICLE_TYPE,
            "legal_intention": ClassificationType.LEGAL_INTENTION,
            "legal_category": ClassificationType.LEGAL_CATEGORY,
            "normative_type": ClassificationType.NORMATIVE_TYPE,
            "title": ClassificationType.TITLE
        }
        
        if classification_type not in type_mapping:
            return json.dumps({"error": f"Tipo de classificação inválido: {classification_type}"}, ensure_ascii=False)
        
        result = classifier.classify_text(text, type_mapping[classification_type])
        
        return json.dumps({
            "classification_type": classification_type,
            "result": result,
            "text_preview": text[:200] + "..." if len(text) > 200 else text
        }, ensure_ascii=False, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Erro na classificação: {str(e)}"}, ensure_ascii=False)


@tool("Comprehensive Legal Analysis Tool")
def comprehensive_legal_analysis_tool(text: str) -> str:
    """
    Ferramenta para análise legal abrangente combinando múltiplas classificações.
    
    Args:
        text: Texto do documento legal para análise completa
        
    Returns:
        JSON string com análise legal completa
    """
    if not ENHANCED_CLASSIFIER_AVAILABLE:
        return json.dumps({
            "error": "Enhanced classifier not available",
            "message": "Required dependencies not installed"
        }, ensure_ascii=False)
    
    try:
        classifier = get_classifier()
        
        results = {
            "text_preview": text[:200] + "..." if len(text) > 200 else text,
            "classifications": {
                "subject": classifier.classify_subject(text),
                "article_type": classifier.classify_article_type(text),
                "legal_intention": classifier.classify_legal_intention(text),
                "legal_category": classifier.classify_legal_category(text),
                "normative_type": classifier.classify_normative_type(text),
                "generated_title": classifier.generate_title(text)
            }
        }
        
        return json.dumps(results, ensure_ascii=False, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Erro na análise legal: {str(e)}"}, ensure_ascii=False)


@tool("Text Preprocessing Tool")
def text_preprocessing_tool(text: str, operations: str = "clean,normalize") -> str:
    """
    Ferramenta para pré-processamento de texto.
    
    Args:
        text: Texto para pré-processamento
        operations: Operações separadas por vírgula (clean, normalize, tokenize, etc.)
        
    Returns:
        JSON string com texto processado
    """
    try:
        import re
        
        processed_text = text
        operations_list = [op.strip() for op in operations.split(",")]
        
        for operation in operations_list:
            if operation == "clean":
                # Remove caracteres especiais desnecessários
                processed_text = re.sub(r'[^\w\s\.\,\;\:\!\?\-]', '', processed_text)
            elif operation == "normalize":
                # Normaliza espaços em branco
                processed_text = re.sub(r'\s+', ' ', processed_text).strip()
            elif operation == "lowercase":
                processed_text = processed_text.lower()
            elif operation == "remove_numbers":
                processed_text = re.sub(r'\d+', '', processed_text)
        
        return json.dumps({
            "original_text": text[:100] + "..." if len(text) > 100 else text,
            "processed_text": processed_text,
            "operations_applied": operations_list
        }, ensure_ascii=False, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Erro no pré-processamento: {str(e)}"}, ensure_ascii=False)


class CrewAINLPAgents:
    """Factory class for creating CrewAI NLP agents"""
    
    def __init__(self, config: CrewAINLPConfiguration = None):
        self.config = config or CrewAINLPConfiguration()
    
    def create_sentiment_agent(self) -> Agent:
        """Create sentiment analysis agent"""
        if not CREWAI_AVAILABLE:
            raise ImportError("CrewAI not available - cannot create agents")
        
        return Agent(
            **self.config.sentiment_agent_config,
            tools=[enhanced_sentiment_analysis_tool, text_preprocessing_tool]
        )
    
    def create_legal_classifier_agent(self) -> Agent:
        """Create legal document classification agent"""
        if not CREWAI_AVAILABLE:
            raise ImportError("CrewAI not available - cannot create agents")
        
        return Agent(
            **self.config.legal_classifier_agent_config,
            tools=[
                legal_document_classification_tool,
                comprehensive_legal_analysis_tool,
                text_preprocessing_tool
            ]
        )
    
    def create_text_analyzer_agent(self) -> Agent:
        """Create advanced text analysis agent"""
        if not CREWAI_AVAILABLE:
            raise ImportError("CrewAI not available - cannot create agents")
        
        file_tools = []
        if CREWAI_TOOLS_AVAILABLE:
            file_tools = [FileReadTool(), FileWriterTool()]
        
        return Agent(
            **self.config.text_analyzer_agent_config,
            tools=[
                enhanced_sentiment_analysis_tool,
                comprehensive_legal_analysis_tool,
                text_preprocessing_tool
            ] + file_tools
        )


class CrewAINLPWorkflows:
    """Pre-defined workflows using CrewAI for common NLP tasks"""
    
    def __init__(self, config: CrewAINLPConfiguration = None):
        self.config = config or CrewAINLPConfiguration()
        self.agents_factory = CrewAINLPAgents(self.config)
    
    def sentiment_analysis_workflow(self, text: str) -> Dict[str, Any]:
        """
        Execute sentiment analysis workflow using CrewAI agents
        
        Args:
            text: Text to analyze
            
        Returns:
            Workflow results including sentiment analysis
        """
        try:
            # Create sentiment agent
            sentiment_agent = self.agents_factory.create_sentiment_agent()
            
            # Define task
            sentiment_task = Task(
                description=f"""
                Analise o sentimento do seguinte texto de forma abrangente:
                
                TEXTO: {text}
                
                Forneça uma análise detalhada incluindo:
                1. Classificação básica de sentimento (Positivo, Negativo, Neutro)
                2. Detecção de emoções específicas
                3. Análise de intensidade e confiança
                4. Análise de subjetividade
                5. Sentimentos baseados em aspectos (se aplicável)
                6. Resumo executivo da análise
                """,
                agent=sentiment_agent,
                expected_output="Análise completa de sentimentos em formato estruturado"
            )
            
            # Create and execute crew
            crew = Crew(
                agents=[sentiment_agent],
                tasks=[sentiment_task],
                verbose=True
            )
            
            result = crew.kickoff()
            
            return {
                "workflow": "sentiment_analysis",
                "input_text": text[:200] + "..." if len(text) > 200 else text,
                "result": str(result),
                "status": "success"
            }
            
        except Exception as e:
            logging.error(f"Erro no workflow de análise de sentimentos: {e}")
            return {
                "workflow": "sentiment_analysis",
                "input_text": text[:200] + "..." if len(text) > 200 else text,
                "error": str(e),
                "status": "error"
            }
    
    def legal_document_analysis_workflow(self, text: str) -> Dict[str, Any]:
        """
        Execute comprehensive legal document analysis workflow
        
        Args:
            text: Legal document text to analyze
            
        Returns:
            Workflow results including legal classification and analysis
        """
        try:
            # Create agents
            legal_agent = self.agents_factory.create_legal_classifier_agent()
            text_agent = self.agents_factory.create_text_analyzer_agent()
            
            # Define tasks
            classification_task = Task(
                description=f"""
                Classifique o seguinte documento legal de forma abrangente:
                
                DOCUMENTO: {text}
                
                Realize as seguintes classificações:
                1. Assunto principal do documento
                2. Tipo de artigo/norma
                3. Intenção legal
                4. Categoria legal
                5. Tipo normativo
                6. Gere um título apropriado
                
                Forneça explicações para cada classificação.
                """,
                agent=legal_agent,
                expected_output="Classificação completa do documento legal com justificativas"
            )
            
            analysis_task = Task(
                description=f"""
                Com base na classificação do documento legal, realize uma análise estrutural detalhada:
                
                DOCUMENTO: {text}
                
                Analise:
                1. Estrutura do documento
                2. Elementos-chave identificados
                3. Padrões textuais relevantes
                4. Recomendações de processamento
                5. Análise de qualidade do texto
                """,
                agent=text_agent,
                expected_output="Análise estrutural e recomendações para o documento",
                context=[classification_task]
            )
            
            # Create and execute crew
            crew = Crew(
                agents=[legal_agent, text_agent],
                tasks=[classification_task, analysis_task],
                verbose=True
            )
            
            result = crew.kickoff()
            
            return {
                "workflow": "legal_document_analysis",
                "input_text": text[:200] + "..." if len(text) > 200 else text,
                "result": str(result),
                "status": "success"
            }
            
        except Exception as e:
            logging.error(f"Erro no workflow de análise legal: {e}")
            return {
                "workflow": "legal_document_analysis",
                "input_text": text[:200] + "..." if len(text) > 200 else text,
                "error": str(e),
                "status": "error"
            }
    
    def comprehensive_nlp_workflow(self, text: str) -> Dict[str, Any]:
        """
        Execute comprehensive NLP workflow combining multiple analyses
        
        Args:
            text: Text to analyze comprehensively
            
        Returns:
            Complete NLP analysis results
        """
        try:
            # Create all agents
            sentiment_agent = self.agents_factory.create_sentiment_agent()
            legal_agent = self.agents_factory.create_legal_classifier_agent()
            text_agent = self.agents_factory.create_text_analyzer_agent()
            
            # Define tasks
            preprocessing_task = Task(
                description=f"""
                Pré-processe o seguinte texto para análise:
                
                TEXTO: {text}
                
                Execute:
                1. Limpeza do texto
                2. Normalização
                3. Identificação de características textuais
                4. Preparação para análises subsequentes
                """,
                agent=text_agent,
                expected_output="Texto pré-processado e relatório de características"
            )
            
            sentiment_task = Task(
                description=f"""
                Analise o sentimento do texto pré-processado:
                
                TEXTO: {text}
                
                Forneça análise completa de sentimentos.
                """,
                agent=sentiment_agent,
                expected_output="Análise completa de sentimentos",
                context=[preprocessing_task]
            )
            
            legal_task = Task(
                description=f"""
                Se o texto for de natureza legal, classifique-o adequadamente:
                
                TEXTO: {text}
                
                Determine se é um documento legal e, se sim, classifique-o.
                """,
                agent=legal_agent,
                expected_output="Classificação legal (se aplicável)",
                context=[preprocessing_task]
            )
            
            synthesis_task = Task(
                description="""
                Sintetize todas as análises realizadas e forneça um relatório executivo:
                
                1. Resumo das análises de sentimento
                2. Resumo das classificações legais
                3. Insights principais
                4. Recomendações
                """,
                agent=text_agent,
                expected_output="Relatório executivo consolidado",
                context=[preprocessing_task, sentiment_task, legal_task]
            )
            
            # Create and execute crew
            crew = Crew(
                agents=[sentiment_agent, legal_agent, text_agent],
                tasks=[preprocessing_task, sentiment_task, legal_task, synthesis_task],
                verbose=True
            )
            
            result = crew.kickoff()
            
            return {
                "workflow": "comprehensive_nlp",
                "input_text": text[:200] + "..." if len(text) > 200 else text,
                "result": str(result),
                "status": "success"
            }
            
        except Exception as e:
            logging.error(f"Erro no workflow NLP abrangente: {e}")
            return {
                "workflow": "comprehensive_nlp",
                "input_text": text[:200] + "..." if len(text) > 200 else text,
                "error": str(e),
                "status": "error"
            }


# Main interface functions for CrewAI NLP
def create_nlp_crew(workflow_type: str = "comprehensive") -> CrewAINLPWorkflows:
    """
    Create NLP crew for specific workflow type
    
    Args:
        workflow_type: Type of workflow (sentiment, legal, comprehensive)
        
    Returns:
        Configured CrewAI NLP workflows instance
    """
    config = CrewAINLPConfiguration()
    return CrewAINLPWorkflows(config)


def analyze_text_with_crewai(text: str, workflow_type: str = "comprehensive") -> Dict[str, Any]:
    """
    Analyze text using CrewAI agents and workflows
    
    Args:
        text: Text to analyze
        workflow_type: Type of analysis workflow
        
    Returns:
        Analysis results from CrewAI workflow
    """
    workflows = create_nlp_crew(workflow_type)
    
    if workflow_type == "sentiment":
        return workflows.sentiment_analysis_workflow(text)
    elif workflow_type == "legal":
        return workflows.legal_document_analysis_workflow(text)
    elif workflow_type == "comprehensive":
        return workflows.comprehensive_nlp_workflow(text)
    else:
        raise ValueError(f"Unsupported workflow type: {workflow_type}")


# Backward compatibility functions that now use CrewAI
def crewai_sentiment_analysis(text: str) -> Dict[str, Any]:
    """CrewAI-powered sentiment analysis with backward compatibility"""
    return analyze_text_with_crewai(text, "sentiment")


def crewai_legal_classification(text: str) -> Dict[str, Any]:
    """CrewAI-powered legal document classification"""
    return analyze_text_with_crewai(text, "legal")