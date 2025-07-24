# flake8: noqa: E501

"""
Módulo CrewAI para análise de textos legislativos.

Este módulo implementa agentes especializados para análise colaborativa
de documentos legislativos usando o framework CrewAI.
"""
from .agents import LegalAnalysisAgent, DocumentReviewAgent, ComplianceAgent
from .tools import (
    LegalContextExtractionTool,
    SubjectSynthesisTool,
    StructuredSummaryTool,
    DocumentArticleAnalysisTool,
    QuestionGenerationTool,
    LegalAssessmentTool,
    ConstitutionalRetrievalTool
)

__all__ = [
    'LegalAnalysisAgent', 
    'DocumentReviewAgent', 
    'ComplianceAgent',
    'LegalAnalysisCrewManager',
    'LegalContextExtractionTool',
    'SubjectSynthesisTool', 
    'StructuredSummaryTool',
    'DocumentArticleAnalysisTool',
    'QuestionGenerationTool',
    'LegalAssessmentTool',
    'ConstitutionalRetrievalTool'
]