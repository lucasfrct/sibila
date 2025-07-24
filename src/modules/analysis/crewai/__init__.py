# CrewAI Integration for Legal Analysis
# This module transforms the traditional analysis functions into CrewAI agents and tools

from .agents import LegalAnalysisCrewManager
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
    'LegalAnalysisCrewManager',
    'LegalContextExtractionTool',
    'SubjectSynthesisTool', 
    'StructuredSummaryTool',
    'DocumentArticleAnalysisTool',
    'QuestionGenerationTool',
    'LegalAssessmentTool',
    'ConstitutionalRetrievalTool'
]