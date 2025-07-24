# Simple test for CrewAI tools functionality

import sys
import os

# Add project path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_tools_directly():
    """Test CrewAI tools directly without agents"""
    print("Testing CrewAI tools directly...")
    
    try:
        from src.modules.nlp.crewai_integration import (
            enhanced_sentiment_analysis_tool,
            legal_document_classification_tool,
            comprehensive_legal_analysis_tool,
            text_preprocessing_tool
        )
        
        sample_text = "Art. 1º É livre a manifestação do pensamento."
        
        print("\n1. Testing sentiment analysis tool...")
        try:
            # Test the actual function behind the tool
            result = enhanced_sentiment_analysis_tool._run(sample_text)
            print(f"✓ Sentiment result: {result[:100]}...")
        except Exception as e:
            print(f"❌ Sentiment error: {e}")
        
        print("\n2. Testing legal classification tool...")
        try:
            result = legal_document_classification_tool._run(sample_text, "subject")
            print(f"✓ Classification result: {result[:100]}...")
        except Exception as e:
            print(f"❌ Classification error: {e}")
        
        print("\n3. Testing comprehensive analysis tool...")
        try:
            result = comprehensive_legal_analysis_tool._run(sample_text)
            print(f"✓ Comprehensive result: {result[:100]}...")
        except Exception as e:
            print(f"❌ Comprehensive error: {e}")
        
        print("\n4. Testing preprocessing tool...")
        try:
            result = text_preprocessing_tool._run(sample_text, "clean,normalize")
            print(f"✓ Preprocessing result: {result[:100]}...")
        except Exception as e:
            print(f"❌ Preprocessing error: {e}")
            
    except ImportError as e:
        print(f"Import error: {e}")
    except Exception as e:
        print(f"General error: {e}")


def test_nlp_module_import():
    """Test importing the NLP module"""
    print("\nTesting NLP module import...")
    
    try:
        from src.modules.nlp import CREWAI_AVAILABLE
        print(f"✓ CrewAI available: {CREWAI_AVAILABLE}")
        
        if CREWAI_AVAILABLE:
            from src.modules.nlp import (
                create_nlp_crew, analyze_text_with_crewai,
                get_available_pipelines
            )
            print("✓ Main CrewAI functions imported successfully")
            
            # Test pipeline info
            pipelines = get_available_pipelines()
            print(f"✓ Available pipelines: {list(pipelines.keys())}")
            
        else:
            print("⚠️ CrewAI integration not available")
            
    except Exception as e:
        print(f"❌ NLP module test error: {e}")


def test_backward_compatibility():
    """Test that existing functionality still works"""
    print("\nTesting backward compatibility...")
    
    try:
        # Test basic classifier
        from src.modules.nlp import classifier
        print("✓ Basic classifier available")
        
        # Test enhanced sentiment
        from src.modules.nlp import sentiment_analysis_enhanced
        result = sentiment_analysis_enhanced("Test text for sentiment analysis")
        print(f"✓ Enhanced sentiment works: {result.get('basic_sentiment', {}).get('classification', 'N/A')}")
        
        # Test enhanced classifier
        from src.modules.nlp import get_classifier
        classifier_instance = get_classifier()
        subject_result = classifier_instance.classify_subject("Art. 1º É livre a manifestação do pensamento.")
        print(f"✓ Enhanced classifier works: {subject_result}")
        
    except Exception as e:
        print(f"❌ Backward compatibility error: {e}")


if __name__ == "__main__":
    print("🧪 TESTE SIMPLES: Funcionalidades CrewAI NLP")
    print("=" * 60)
    
    test_tools_directly()
    test_nlp_module_import()
    test_backward_compatibility()
    
    print("\n" + "=" * 60)
    print("✅ TESTE CONCLUÍDO")