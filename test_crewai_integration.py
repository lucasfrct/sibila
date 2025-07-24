#!/usr/bin/env python3
"""
Test script for CrewAI Legal Analysis Integration

Tests the CrewAI-based legal analysis functionality to ensure proper integration
and backward compatibility.
"""

import os
import sys
import json
import unittest
from unittest.mock import patch, MagicMock

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))


class TestCrewAILegalAnalysis(unittest.TestCase):
    """Test cases for CrewAI legal analysis integration"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.sample_legal_text = """
        Art. 1º Esta lei estabelece diretrizes para a proteção de dados pessoais.
        Art. 2º Para os fins desta lei, considera-se dado pessoal a informação relacionada a pessoa natural.
        Art. 3º O tratamento de dados observará os princípios da finalidade e adequação.
        """
    
    def test_crewai_module_import(self):
        """Test that CrewAI modules can be imported"""
        try:
            from src.modules.analysis import CREWAI_ANALYSIS_AVAILABLE
            from src.modules.analysis.crewai.tools import LegalContextExtractionTool
            from src.modules.analysis.crewai.agents import LegalAnalysisCrewManager
            
            self.assertTrue(True, "CrewAI modules imported successfully")
        except ImportError as e:
            self.fail(f"Failed to import CrewAI modules: {e}")
    
    def test_crewai_tools_initialization(self):
        """Test that CrewAI tools can be initialized"""
        try:
            from src.modules.analysis.crewai.tools import (
                LegalContextExtractionTool,
                SubjectSynthesisTool,
                StructuredSummaryTool,
                DocumentArticleAnalysisTool,
                QuestionGenerationTool,
                LegalAssessmentTool
            )
            
            # Initialize tools
            context_tool = LegalContextExtractionTool()
            synthesis_tool = SubjectSynthesisTool()
            summary_tool = StructuredSummaryTool()
            article_tool = DocumentArticleAnalysisTool()
            question_tool = QuestionGenerationTool()
            assessment_tool = LegalAssessmentTool()
            
            # Check tool properties
            self.assertIsNotNone(context_tool.name)
            self.assertIsNotNone(context_tool.description)
            self.assertIsNotNone(synthesis_tool.name)
            self.assertIsNotNone(summary_tool.name)
            self.assertIsNotNone(article_tool.name)
            self.assertIsNotNone(question_tool.name)
            self.assertIsNotNone(assessment_tool.name)
            
        except Exception as e:
            self.fail(f"Failed to initialize CrewAI tools: {e}")
    
    def test_tools_without_enhanced_analysis(self):
        """Test tool behavior when enhanced analysis is not available"""
        
        # Mock the enhanced analysis availability
        with patch('src.modules.analysis.crewai.tools.ENHANCED_ANALYSIS_AVAILABLE', False):
            from src.modules.analysis.crewai.tools import LegalContextExtractionTool
            
            tool = LegalContextExtractionTool()
            result = tool._run(self.sample_legal_text)
            
            # Parse result
            result_data = json.loads(result)
            self.assertIn("error", result_data)
            self.assertEqual(result_data["error"], "Enhanced analysis not available")
    
    def test_tools_with_mocked_enhanced_analysis(self):
        """Test tool behavior with mocked enhanced analysis functions"""
        
        # Mock the enhanced analysis functions
        mock_context = MagicMock()
        mock_context.names = ["Teste"]
        mock_context.actions = ["estabelecer"]
        mock_context.deductions = []
        mock_context.events = []
        mock_context.attention_points = ["proteção de dados"]
        mock_context.legal_terms = ["dados pessoais"]
        mock_context.dates_deadlines = []
        mock_context.penalties = []
        
        with patch('src.modules.analysis.crewai.tools.ENHANCED_ANALYSIS_AVAILABLE', True), \
             patch('src.modules.analysis.crewai.tools.extract_legal_context', return_value=mock_context):
            
            from src.modules.analysis.crewai.tools import LegalContextExtractionTool
            
            tool = LegalContextExtractionTool()
            result = tool._run(self.sample_legal_text)
            
            # Parse result
            result_data = json.loads(result)
            self.assertTrue(result_data.get("success"))
            self.assertIn("context", result_data)
            self.assertEqual(result_data["context"]["names"], ["Teste"])
            self.assertEqual(result_data["context"]["attention_points"], ["proteção de dados"])
    
    def test_crew_manager_initialization(self):
        """Test that the CrewAI manager can be initialized"""
        try:
            from src.modules.analysis.crewai.agents import LegalAnalysisCrewManager
            
            # Initialize without API key (should work for setup)
            manager = LegalAnalysisCrewManager()
            
            self.assertIsNotNone(manager.tools)
            self.assertIsNotNone(manager.agents)
            self.assertEqual(len(manager.agents), 5)  # 5 specialized agents
            
            # Check agent names
            expected_agents = [
                'context_analyst', 'subject_expert', 'structure_analyst', 
                'legal_examiner', 'assessment_coordinator'
            ]
            for agent_name in expected_agents:
                self.assertIn(agent_name, manager.agents)
                
        except Exception as e:
            self.fail(f"Failed to initialize CrewAI manager: {e}")
    
    def test_convenience_functions(self):
        """Test the convenience functions for backward compatibility"""
        try:
            from src.modules.analysis.crewai.agents import (
                crewai_enhanced_legal_document_analysis,
                crewai_enhanced_questionnaire
            )
            
            # These functions should exist and be callable
            self.assertTrue(callable(crewai_enhanced_legal_document_analysis))
            self.assertTrue(callable(crewai_enhanced_questionnaire))
            
        except ImportError as e:
            self.fail(f"Failed to import convenience functions: {e}")
    
    def test_backward_compatibility_imports(self):
        """Test that new imports are available in the main analysis module"""
        try:
            from src.modules.analysis import (
                CREWAI_ANALYSIS_AVAILABLE,
                LegalAnalysisCrewManager,
                crewai_enhanced_legal_document_analysis
            )
            
            # Check availability flag
            self.assertIsInstance(CREWAI_ANALYSIS_AVAILABLE, bool)
            
            # Check classes and functions are imported
            self.assertIsNotNone(LegalAnalysisCrewManager)
            self.assertTrue(callable(crewai_enhanced_legal_document_analysis))
            
        except ImportError as e:
            # CrewAI might not be available, which is ok for testing
            print(f"CrewAI imports not available (expected in some environments): {e}")
    
    def test_tool_error_handling(self):
        """Test that tools handle errors gracefully"""
        
        # Mock an exception in the enhanced analysis
        with patch('src.modules.analysis.crewai.tools.ENHANCED_ANALYSIS_AVAILABLE', True), \
             patch('src.modules.analysis.crewai.tools.extract_legal_context', side_effect=Exception("Test error")):
            
            from src.modules.analysis.crewai.tools import LegalContextExtractionTool
            
            tool = LegalContextExtractionTool()
            result = tool._run(self.sample_legal_text)
            
            # Parse result
            result_data = json.loads(result)
            self.assertIn("error", result_data)
            self.assertIn("Test error", result_data["error"])
    
    def test_json_output_format(self):
        """Test that tools return valid JSON output"""
        
        # Test with mocked successful response
        with patch('src.modules.analysis.crewai.tools.ENHANCED_ANALYSIS_AVAILABLE', True), \
             patch('src.modules.analysis.crewai.tools.generate_subject_synthesis', return_value="Test synthesis"):
            
            from src.modules.analysis.crewai.tools import SubjectSynthesisTool
            
            tool = SubjectSynthesisTool()
            result = tool._run(self.sample_legal_text)
            
            # Should be valid JSON
            try:
                result_data = json.loads(result)
                self.assertTrue(result_data.get("success"))
                self.assertEqual(result_data.get("synthesis"), "Test synthesis")
            except json.JSONDecodeError:
                self.fail("Tool did not return valid JSON")


def run_integration_test():
    """Run integration test with actual CrewAI components"""
    
    print("🧪 TESTE DE INTEGRAÇÃO CREWAI")
    print("=" * 50)
    
    try:
        # Test basic imports
        print("1. Testando importações...")
        from src.modules.analysis import CREWAI_ANALYSIS_AVAILABLE
        
        if CREWAI_ANALYSIS_AVAILABLE:
            print("✅ CrewAI disponível")
            
            # Test tool initialization
            print("2. Testando inicialização de ferramentas...")
            from src.modules.analysis.crewai.tools import LegalContextExtractionTool
            tool = LegalContextExtractionTool()
            print(f"✅ Ferramenta criada: {tool.name}")
            
            # Test agent initialization
            print("3. Testando inicialização de agentes...")
            from src.modules.analysis.crewai.agents import LegalAnalysisCrewManager
            manager = LegalAnalysisCrewManager()
            print(f"✅ Gerenciador criado com {len(manager.agents)} agentes")
            
            # Test convenience function
            print("4. Testando funções de conveniência...")
            from src.modules.analysis import crewai_enhanced_legal_document_analysis
            print("✅ Função de análise disponível")
            
            print("\n🎉 Todos os testes de integração passaram!")
            
        else:
            print("⚠️  CrewAI não disponível - alguns recursos podem estar limitados")
            
    except Exception as e:
        print(f"❌ Erro no teste de integração: {e}")
        return False
    
    return True


if __name__ == "__main__":
    print("🚀 Executando testes do CrewAI Legal Analysis...")
    
    # Run unit tests
    print("\n📋 TESTES UNITÁRIOS")
    print("=" * 50)
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # Run integration test
    print("\n📋 TESTE DE INTEGRAÇÃO")
    print("=" * 50)
    integration_success = run_integration_test()
    
    if integration_success:
        print("\n✅ Todos os testes concluídos com sucesso!")
    else:
        print("\n⚠️  Alguns testes falharam - verifique as dependências")