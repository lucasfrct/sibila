# Analysis module initialization

# Import enhanced legal analysis functionality
try:
    from .enhanced_legal_analysis import (
        enhanced_legal_document_analysis,
        analyze_long_legal_text,
        check_service_integration,
        extract_legal_context,
        generate_subject_synthesis,
        generate_structured_summary,
        format_synthesis_report,
        LegalSynthesis,
        LegalContext
    )
    ENHANCED_ANALYSIS_AVAILABLE = True
except ImportError as e:
    ENHANCED_ANALYSIS_AVAILABLE = False
    print(f"Enhanced legal analysis not available: {e}")

# Import existing analysis modules
try:
    from . import examining_board
    from . import legislation
    from . import federal_constitution_retrieval
    LEGACY_ANALYSIS_AVAILABLE = True
except ImportError as e:
    LEGACY_ANALYSIS_AVAILABLE = False
    print(f"Legacy analysis modules not available: {e}")

__all__ = [
    # Enhanced analysis functions
    'enhanced_legal_document_analysis',
    'analyze_long_legal_text', 
    'check_service_integration',
    'extract_legal_context',
    'generate_subject_synthesis',
    'generate_structured_summary',
    'format_synthesis_report',
    'LegalSynthesis',
    'LegalContext',
    
    # Legacy modules
    'examining_board',
    'legislation', 
    'federal_constitution_retrieval',
    
    # Status flags
    'ENHANCED_ANALYSIS_AVAILABLE',
    'LEGACY_ANALYSIS_AVAILABLE'
]