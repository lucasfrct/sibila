# Test for CrewAI NLP Integration
# Validates CrewAI agents, tools, and workflows

import unittest
import sys
import os
import logging
from unittest.mock import patch, MagicMock

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

# Configure logging for tests
logging.basicConfig(level=logging.WARNING)


class TestCrewAINLPIntegration(unittest.TestCase):
    """Test cases for CrewAI NLP integration"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.sample_text = """
        Art. 1º É livre a manifestação do pensamento, sendo vedado o anonimato.
        Art. 2º Ninguém será obrigado a fazer ou deixar de fazer alguma coisa senão em virtude de lei.
        Art. 3º A lei não prejudicará o direito adquirido, o ato jurídico perfeito e a coisa julgada.
        """
        
        self.sample_legal_text = """
        LEI Nº 12.965, DE 23 DE ABRIL DE 2014.
        
        Estabelece princípios, garantias, direitos e deveres para o uso da Internet no Brasil.
        
        O PRESIDENTE DA REPÚBLICA Faço saber que o Congresso Nacional decreta e eu sanciono a seguinte Lei:
        
        Art. 1º Esta Lei estabelece princípios, garantias, direitos e deveres para o uso da internet no Brasil e determina as diretrizes para atuação da União, dos Estados, do Distrito Federal e dos Municípios em relação à matéria.
        """
    
    def test_import_crewai_modules(self):
        """Test that CrewAI modules can be imported successfully"""
        try:
            from src.modules.nlp.crewai_integration import (
                CrewAINLPConfiguration, CrewAINLPAgents, CrewAINLPWorkflows
            )
            from src.modules.nlp.crewai_config import CrewAINLPConfig
            from src.modules.nlp.crewai_pipeline import CrewAIPipelineManager
            self.assertTrue(True, "All CrewAI modules imported successfully")
        except ImportError as e:
            self.fail(f"Failed to import CrewAI modules: {e}")
    
    def test_crewai_configuration(self):
        """Test CrewAI configuration setup"""
        try:
            from src.modules.nlp.crewai_config import CrewAINLPConfig, validate_environment
            
            # Test configuration creation
            config = CrewAINLPConfig()
            self.assertIsNotNone(config.AGENT_ROLES)
            self.assertIsNotNone(config.WORKFLOW_CONFIGS)
            self.assertIsNotNone(config.TOOL_CONFIGS)
            
            # Test environment validation (may fail if dependencies not installed)
            validation_results = validate_environment()
            self.assertIsInstance(validation_results, dict)
            
        except Exception as e:
            self.fail(f"CrewAI configuration test failed: {e}")
    
    def test_sentiment_analysis_tool(self):
        """Test sentiment analysis tool functionality"""
        try:
            from src.modules.nlp.crewai_integration import enhanced_sentiment_analysis_tool
            
            # Mock the actual analysis to avoid dependency issues
            with patch('src.modules.nlp.crewai_integration.EnhancedSentimentAnalyzer') as mock_analyzer:
                mock_instance = MagicMock()
                mock_instance.analyze_comprehensive.return_value = {
                    "basic_sentiment": {"classification": "Neutral", "polarity": 0.0},
                    "emotions": {"dominant_emotion": "neutral"},
                    "confidence": 0.8
                }
                mock_analyzer.return_value = mock_instance
                
                result = enhanced_sentiment_analysis_tool(self.sample_text)
                self.assertIsInstance(result, str)
                # Should return JSON string
                import json
                parsed_result = json.loads(result)
                self.assertIn("basic_sentiment", parsed_result)
                
        except Exception as e:
            self.fail(f"Sentiment analysis tool test failed: {e}")
    
    def test_legal_classification_tool(self):
        """Test legal document classification tool"""
        try:
            from src.modules.nlp.crewai_integration import legal_document_classification_tool
            
            # Mock the classifier to avoid dependency issues
            with patch('src.modules.nlp.crewai_integration.get_classifier') as mock_get_classifier:
                mock_classifier = MagicMock()
                mock_classifier.classify_text.return_value = "Direitos Fundamentais"
                mock_get_classifier.return_value = mock_classifier
                
                result = legal_document_classification_tool(self.sample_legal_text, "subject")
                self.assertIsInstance(result, str)
                
                # Should return JSON string
                import json
                parsed_result = json.loads(result)
                self.assertIn("classification_type", parsed_result)
                self.assertIn("result", parsed_result)
                
        except Exception as e:
            self.fail(f"Legal classification tool test failed: {e}")
    
    def test_text_preprocessing_tool(self):
        """Test text preprocessing tool"""
        try:
            from src.modules.nlp.crewai_integration import text_preprocessing_tool
            
            result = text_preprocessing_tool(self.sample_text, "clean,normalize")
            self.assertIsInstance(result, str)
            
            # Should return JSON string
            import json
            parsed_result = json.loads(result)
            self.assertIn("processed_text", parsed_result)
            self.assertIn("operations_applied", parsed_result)
            
        except Exception as e:
            self.fail(f"Text preprocessing tool test failed: {e}")
    
    def test_agents_factory(self):
        """Test CrewAI agents factory"""
        try:
            from src.modules.nlp.crewai_integration import CrewAINLPAgents
            
            agents_factory = CrewAINLPAgents()
            
            # Test agent creation (mock CrewAI Agent class)
            with patch('src.modules.nlp.crewai_integration.Agent') as mock_agent:
                mock_agent.return_value = MagicMock()
                
                sentiment_agent = agents_factory.create_sentiment_agent()
                legal_agent = agents_factory.create_legal_classifier_agent()
                text_agent = agents_factory.create_text_analyzer_agent()
                
                self.assertIsNotNone(sentiment_agent)
                self.assertIsNotNone(legal_agent)
                self.assertIsNotNone(text_agent)
                
        except Exception as e:
            self.fail(f"Agents factory test failed: {e}")
    
    def test_workflow_creation(self):
        """Test workflow creation and setup"""
        try:
            from src.modules.nlp.crewai_integration import CrewAINLPWorkflows
            
            workflows = CrewAINLPWorkflows()
            
            # Test workflow methods exist
            self.assertTrue(hasattr(workflows, 'sentiment_analysis_workflow'))
            self.assertTrue(hasattr(workflows, 'legal_document_analysis_workflow'))
            self.assertTrue(hasattr(workflows, 'comprehensive_nlp_workflow'))
            
        except Exception as e:
            self.fail(f"Workflow creation test failed: {e}")
    
    def test_pipeline_manager(self):
        """Test pipeline manager functionality"""
        try:
            from src.modules.nlp.crewai_pipeline import CrewAIPipelineManager
            
            manager = CrewAIPipelineManager()
            
            # Test pipeline creation
            legal_pipeline = manager.create_legal_document_pipeline()
            batch_pipeline = manager.create_batch_processing_pipeline()
            
            self.assertIsInstance(legal_pipeline, dict)
            self.assertIsInstance(batch_pipeline, dict)
            
            self.assertIn("pipeline_id", legal_pipeline)
            self.assertIn("tasks", legal_pipeline)
            self.assertIn("pipeline_id", batch_pipeline)
            self.assertIn("tasks", batch_pipeline)
            
        except Exception as e:
            self.fail(f"Pipeline manager test failed: {e}")
    
    def test_nlp_module_integration(self):
        """Test that NLP module properly exposes CrewAI functionality"""
        try:
            # Test main module imports
            from src.modules.nlp import (
                create_nlp_crew, analyze_text_with_crewai,
                crewai_sentiment_analysis, crewai_legal_classification
            )
            
            # Test that functions exist and are callable
            self.assertTrue(callable(create_nlp_crew))
            self.assertTrue(callable(analyze_text_with_crewai))
            self.assertTrue(callable(crewai_sentiment_analysis))
            self.assertTrue(callable(crewai_legal_classification))
            
        except ImportError as e:
            # This is expected if CrewAI is not available
            self.skipTest(f"CrewAI not available in main module: {e}")
    
    def test_backward_compatibility(self):
        """Test that existing NLP functionality still works"""
        try:
            # Test that existing functions are still available
            from src.modules.nlp import (
                classifier, SimpleLegalClassifier, get_simple_classifier
            )
            
            # These should exist regardless of CrewAI availability
            self.assertTrue(callable(classifier))
            self.assertTrue(callable(get_simple_classifier))
            
        except ImportError as e:
            self.fail(f"Backward compatibility broken: {e}")
    
    def test_mock_workflow_execution(self):
        """Test workflow execution with mocked CrewAI components"""
        try:
            from src.modules.nlp.crewai_integration import analyze_text_with_crewai
            
            # Mock the entire CrewAI execution
            with patch('src.modules.nlp.crewai_integration.Crew') as mock_crew_class:
                mock_crew = MagicMock()
                mock_crew.kickoff.return_value = "Mocked analysis result"
                mock_crew_class.return_value = mock_crew
                
                # Mock Agent class
                with patch('src.modules.nlp.crewai_integration.Agent') as mock_agent_class:
                    mock_agent_class.return_value = MagicMock()
                    
                    # Mock Task class
                    with patch('src.modules.nlp.crewai_integration.Task') as mock_task_class:
                        mock_task_class.return_value = MagicMock()
                        
                        # Test sentiment workflow
                        result = analyze_text_with_crewai(self.sample_text, "sentiment")
                        
                        self.assertIsInstance(result, dict)
                        self.assertIn("workflow", result)
                        self.assertIn("status", result)
                        
        except Exception as e:
            self.fail(f"Mock workflow execution test failed: {e}")


class TestCrewAITools(unittest.TestCase):
    """Test cases for individual CrewAI tools"""
    
    def test_tool_decorators(self):
        """Test that tool decorators work correctly"""
        try:
            from src.modules.nlp.crewai_integration import (
                enhanced_sentiment_analysis_tool,
                legal_document_classification_tool,
                comprehensive_legal_analysis_tool,
                text_preprocessing_tool
            )
            
            # Check that functions have tool attributes (added by @tool decorator)
            tools = [
                enhanced_sentiment_analysis_tool,
                legal_document_classification_tool,
                comprehensive_legal_analysis_tool,
                text_preprocessing_tool
            ]
            
            for tool_func in tools:
                # Tool decorator should add metadata
                self.assertTrue(callable(tool_func))
                # The @tool decorator from CrewAI should add attributes
                # We can't test this fully without CrewAI, but we can test they're callable
                
        except Exception as e:
            self.fail(f"Tool decorators test failed: {e}")


if __name__ == '__main__':
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestCrewAINLPIntegration))
    test_suite.addTest(unittest.makeSuite(TestCrewAITools))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\nTest Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")