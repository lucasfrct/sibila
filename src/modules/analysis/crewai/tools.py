"""
CrewAI Tools for Legal Analysis

Transforms existing legal analysis functions into CrewAI tools that can be used by agents.
Each tool provides clear input/output interfaces and error handling for CrewAI integration.
"""

import logging
import json
from typing import Dict, List, Optional, Any

# Conditional import of pydantic
try:
    from pydantic import BaseModel, Field
    PYDANTIC_AVAILABLE = True
except ImportError:
    PYDANTIC_AVAILABLE = False
    # Create dummy classes for type hints
    class BaseModel:
        pass
    def Field(*args, **kwargs):
        return None

# Conditional import of CrewAI tools
try:
    from crewai_tools import BaseTool
    CREWAI_TOOLS_AVAILABLE = True
except ImportError:
    CREWAI_TOOLS_AVAILABLE = False
    # Create a dummy BaseTool class for type hints
    class BaseTool:
        name: str = ""
        description: str = ""
        def _run(self, *args, **kwargs):
            pass

# Import existing analysis functions
try:
    from src.modules.analysis.enhanced_legal_analysis import (
        extract_legal_context,
        generate_subject_synthesis,
        generate_structured_summary,
        analyze_document_articles,
        generate_overall_assessment,
        LegalContext,
        LegalSynthesis
    )
    ENHANCED_ANALYSIS_AVAILABLE = True
except ImportError:
    ENHANCED_ANALYSIS_AVAILABLE = False
    logging.warning("Enhanced legal analysis functions not available")

try:
    from src.modules.analysis.examining_board import (
        question_maker,
        questionnaire,
        ask_a_question
    )
    EXAMINING_BOARD_AVAILABLE = True
except ImportError:
    EXAMINING_BOARD_AVAILABLE = False
    logging.warning("Examining board functions not available")

try:
    from src.modules.analysis.federal_constitution_retrieval import (
        query_by_constellation
    )
    CONSTITUTION_AVAILABLE = True
except ImportError:
    CONSTITUTION_AVAILABLE = False
    logging.warning("Constitutional retrieval not available")

try:
    from src.modules.analysis import legislation as LegislationAnalysis
    LEGISLATION_AVAILABLE = True
except ImportError:
    LEGISLATION_AVAILABLE = False
    logging.warning("Legislation analysis not available")


class LegalDocumentInput(BaseModel):
    """Input schema for legal document analysis tools"""
    text: str = Field(..., description="The legal document text to analyze")
    document_path: Optional[str] = Field(None, description="Optional path to the document file")
    context: Optional[str] = Field(None, description="Additional context for analysis")


class QuestionInput(BaseModel):
    """Input schema for question-related tools"""
    text: str = Field(..., description="The text to generate questions about")
    question: Optional[str] = Field(None, description="Specific question to ask")
    documents: Optional[str] = Field(None, description="Supporting documents for context")


class LegalContextExtractionTool(BaseTool):
    """
    Tool for extracting legal context from documents including entities, actions, 
    deductions, events, and attention points.
    
    Input: Legal document text
    Output: Structured legal context with categorized information
    """
    name: str = "Legal Context Extraction"
    description: str = """
    Extracts comprehensive legal context from legal documents including:
    - Names of people, entities, and organizations
    - Legal actions and procedures  
    - Deductions and legal conclusions
    - Important events and dates
    - Critical attention points
    - Legal terms and penalties
    
    Input: Legal document text (string)
    Output: JSON with categorized legal context information
    """

    def _run(self, text: str) -> str:
        """Extract legal context from the provided text"""
        if not ENHANCED_ANALYSIS_AVAILABLE:
            return json.dumps({
                "error": "Enhanced analysis not available",
                "context": {
                    "names": [],
                    "actions": [],
                    "deductions": [],
                    "events": [],
                    "attention_points": [],
                    "legal_terms": [],
                    "dates_deadlines": [],
                    "penalties": []
                }
            })
        
        try:
            context = extract_legal_context(text)
            return json.dumps({
                "success": True,
                "context": {
                    "names": context.names,
                    "actions": context.actions,
                    "deductions": context.deductions,
                    "events": context.events,
                    "attention_points": context.attention_points,
                    "legal_terms": context.legal_terms,
                    "dates_deadlines": context.dates_deadlines,
                    "penalties": context.penalties
                }
            })
        except Exception as e:
            logging.error(f"Error in legal context extraction: {e}")
            return json.dumps({"error": f"Failed to extract legal context: {str(e)}"})


class SubjectSynthesisTool(BaseTool):
    """
    Tool for generating concise synthesis of the main legal subject/topic.
    
    Input: Legal document text
    Output: Clear and objective synthesis of the main legal subject
    """
    name: str = "Subject Synthesis Generator"
    description: str = """
    Generates a clear and objective synthesis of the main legal subject/topic from legal documents.
    Provides a concise summary that captures the essence of the legal matter being addressed.
    
    Input: Legal document text (string)
    Output: Concise synthesis of the main legal subject (string)
    """

    def _run(self, text: str) -> str:
        """Generate subject synthesis from the provided text"""
        if not ENHANCED_ANALYSIS_AVAILABLE:
            return json.dumps({
                "error": "Enhanced analysis not available",
                "synthesis": "Subject synthesis unavailable - analysis module not found"
            })
        
        try:
            synthesis = generate_subject_synthesis(text)
            return json.dumps({
                "success": True,
                "synthesis": synthesis
            })
        except Exception as e:
            logging.error(f"Error in subject synthesis: {e}")
            return json.dumps({"error": f"Failed to generate subject synthesis: {str(e)}"})


class StructuredSummaryTool(BaseTool):
    """
    Tool for generating structured summaries of legal documents with organized sections.
    
    Input: Legal document text and optional articles analysis
    Output: Hierarchically organized summary with clear sections
    """
    name: str = "Structured Summary Generator"
    description: str = """
    Creates structured summaries of legal documents organized in hierarchical sections.
    Breaks down complex legal content into logical, easy-to-understand sections with titles and subtopics.
    
    Input: Legal document text (string), optional articles_analysis (JSON string)
    Output: Structured summary with organized sections and subtopics
    """

    def _run(self, text: str, articles_analysis: Optional[str] = None) -> str:
        """Generate structured summary from the provided text"""
        if not ENHANCED_ANALYSIS_AVAILABLE:
            return json.dumps({
                "error": "Enhanced analysis not available", 
                "summary": "Structured summary unavailable - analysis module not found"
            })
        
        try:
            # Parse articles analysis if provided
            parsed_articles = None
            if articles_analysis:
                try:
                    parsed_articles = json.loads(articles_analysis)
                except json.JSONDecodeError:
                    logging.warning("Invalid JSON in articles_analysis parameter")
            
            summary = generate_structured_summary(text, parsed_articles)
            return json.dumps({
                "success": True,
                "summary": summary
            })
        except Exception as e:
            logging.error(f"Error in structured summary: {e}")
            return json.dumps({"error": f"Failed to generate structured summary: {str(e)}"})


class DocumentArticleAnalysisTool(BaseTool):
    """
    Tool for analyzing individual articles within legal documents.
    
    Input: Legal document text and optional document path
    Output: Detailed analysis of each article with titles, categories, and summaries
    """
    name: str = "Document Article Analyzer"
    description: str = """
    Analyzes individual articles within legal documents, providing detailed information for each article including:
    - Article titles and numbering
    - Legal categories and classifications
    - Individual article summaries
    - Normative types and components
    
    Input: Legal document text (string), optional document_path (string)
    Output: JSON array with detailed analysis of each article
    """

    def _run(self, text: str, document_path: Optional[str] = None) -> str:
        """Analyze individual articles in the document"""
        if not ENHANCED_ANALYSIS_AVAILABLE:
            return json.dumps({
                "error": "Enhanced analysis not available",
                "articles": []
            })
        
        try:
            articles_analysis = analyze_document_articles(text, document_path)
            return json.dumps({
                "success": True,
                "articles_count": len(articles_analysis),
                "articles": articles_analysis
            })
        except Exception as e:
            logging.error(f"Error in article analysis: {e}")
            return json.dumps({"error": f"Failed to analyze articles: {str(e)}"})


class QuestionGenerationTool(BaseTool):
    """
    Tool for generating legal questions and creating questionnaires based on legal content.
    
    Input: Legal text or article
    Output: Generated questions or complete questionnaire with answers
    """
    name: str = "Legal Question Generator"
    description: str = """
    Generates legal questions and creates comprehensive questionnaires based on legal content.
    Can create both individual questions and complete questionnaires with answers.
    
    Input: Legal text/article (string), mode ('question'|'questionnaire')
    Output: Generated questions or complete questionnaire with prompt-completion pairs
    """

    def _run(self, text: str, mode: str = "question") -> str:
        """Generate questions or questionnaire based on the text"""
        if not EXAMINING_BOARD_AVAILABLE:
            return json.dumps({
                "error": "Examining board not available",
                "questions": []
            })
        
        try:
            if mode == "questionnaire":
                # Generate complete questionnaire
                questionnaire_result = questionnaire(text)
                return json.dumps({
                    "success": True,
                    "mode": "questionnaire",
                    "questions_count": len(questionnaire_result),
                    "questionnaire": questionnaire_result
                })
            else:
                # Generate single question
                question = question_maker(text)
                return json.dumps({
                    "success": True,
                    "mode": "question",
                    "question": question
                })
        except Exception as e:
            logging.error(f"Error in question generation: {e}")
            return json.dumps({"error": f"Failed to generate questions: {str(e)}"})


class LegalAssessmentTool(BaseTool):
    """
    Tool for generating comprehensive legal assessments and evaluations.
    
    Input: Legal document text, legal context, and articles analysis
    Output: Overall assessment with complexity analysis and recommendations
    """
    name: str = "Legal Assessment Generator"
    description: str = """
    Generates comprehensive legal assessments considering document structure, content complexity, 
    legal relevance, and practical implications. Provides professional evaluation and recommendations.
    
    Input: Legal text (string), legal_context (JSON), articles_analysis (JSON)
    Output: Comprehensive legal assessment with evaluation and recommendations
    """

    def _run(self, text: str, legal_context: Optional[str] = None, articles_analysis: Optional[str] = None) -> str:
        """Generate overall legal assessment"""
        if not ENHANCED_ANALYSIS_AVAILABLE:
            return json.dumps({
                "error": "Enhanced analysis not available",
                "assessment": "Legal assessment unavailable - analysis module not found"
            })
        
        try:
            # Parse context if provided
            context_obj = None
            if legal_context:
                try:
                    context_data = json.loads(legal_context)
                    # Create LegalContext object from parsed data
                    if "context" in context_data:
                        ctx = context_data["context"]
                        context_obj = LegalContext(
                            names=ctx.get("names", []),
                            actions=ctx.get("actions", []),
                            deductions=ctx.get("deductions", []),
                            events=ctx.get("events", []),
                            attention_points=ctx.get("attention_points", []),
                            legal_terms=ctx.get("legal_terms", []),
                            dates_deadlines=ctx.get("dates_deadlines", []),
                            penalties=ctx.get("penalties", [])
                        )
                except (json.JSONDecodeError, KeyError):
                    logging.warning("Invalid legal context format")
            
            # Parse articles analysis if provided
            parsed_articles = []
            if articles_analysis:
                try:
                    articles_data = json.loads(articles_analysis)
                    if "articles" in articles_data:
                        parsed_articles = articles_data["articles"]
                except json.JSONDecodeError:
                    logging.warning("Invalid articles analysis format")
            
            # Use empty context if none provided
            if context_obj is None:
                context_obj = LegalContext([], [], [], [], [], [], [], [])
            
            assessment = generate_overall_assessment(text, context_obj, parsed_articles)
            return json.dumps({
                "success": True,
                "assessment": assessment
            })
        except Exception as e:
            logging.error(f"Error in legal assessment: {e}")
            return json.dumps({"error": f"Failed to generate assessment: {str(e)}"})


class ConstitutionalRetrievalTool(BaseTool):
    """
    Tool for retrieving relevant constitutional information based on queries.
    
    Input: Query string and optional parameters
    Output: Relevant constitutional documents and passages
    """
    name: str = "Constitutional Information Retrieval"
    description: str = """
    Retrieves relevant constitutional information and documents based on legal queries.
    Searches the federal constitution database for relevant passages and context.
    
    Input: Query string (string), results_limit (integer, optional), threshold (float, optional)
    Output: Relevant constitutional passages and metadata
    """

    def _run(self, query: str, results_limit: int = 5, threshold: float = 0.5) -> str:
        """Retrieve constitutional information based on query"""
        if not CONSTITUTION_AVAILABLE:
            return json.dumps({
                "error": "Constitutional retrieval not available",
                "results": []
            })
        
        try:
            results = query_by_constellation(query, results_limit, threshold)
            return json.dumps({
                "success": True,
                "query": query,
                "results_count": len(results),
                "results": results
            })
        except Exception as e:
            logging.error(f"Error in constitutional retrieval: {e}")
            return json.dumps({"error": f"Failed to retrieve constitutional information: {str(e)}"})


class QuestionAnsweringTool(BaseTool):
    """
    Tool for answering legal questions based on provided documents and context.
    
    Input: Question, documents, and article context
    Output: Legal answer based on provided documentation
    """
    name: str = "Legal Question Answering"
    description: str = """
    Answers legal questions based on provided documents and article context.
    Uses document context to provide accurate, source-based legal responses.
    
    Input: Question (string), documents (string), article (string)
    Output: Legal answer based on provided documentation
    """

    def _run(self, question: str, documents: str, article: str) -> str:
        """Answer legal question based on provided context"""
        if not EXAMINING_BOARD_AVAILABLE:
            return json.dumps({
                "error": "Question answering not available",
                "answer": "Question answering service unavailable"
            })
        
        try:
            answer = ask_a_question(documents, article, question)
            return json.dumps({
                "success": True,
                "question": question,
                "answer": answer,
                "based_on_article": article[:100] + "..." if len(article) > 100 else article
            })
        except Exception as e:
            logging.error(f"Error in question answering: {e}")
            return json.dumps({"error": f"Failed to answer question: {str(e)}"})