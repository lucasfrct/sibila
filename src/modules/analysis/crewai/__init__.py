# flake8: noqa: E501

"""
Módulo CrewAI para análise de textos legislativos.

Este módulo implementa agentes especializados para análise colaborativa
de documentos legislativos usando o framework CrewAI.
"""

from .agents import LegalAnalysisAgent, DocumentReviewAgent, ComplianceAgent

__all__ = ['LegalAnalysisAgent', 'DocumentReviewAgent', 'ComplianceAgent']