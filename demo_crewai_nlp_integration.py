# Demo: CrewAI Integration for NLP Legal Document Processing
# Demonstrates the new CrewAI-powered NLP capabilities

import sys
import os
import json
import logging
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def demo_basic_crewai_functionality():
    """Demonstrate basic CrewAI NLP functionality"""
    print("=" * 80)
    print("DEMO: CrewAI NLP Integration - Funcionalidades Básicas")
    print("=" * 80)
    
    try:
        from src.modules.nlp import (
            CREWAI_AVAILABLE, validate_environment, get_configuration_summary
        )
        
        print(f"✓ CrewAI disponível: {CREWAI_AVAILABLE}")
        
        if CREWAI_AVAILABLE:
            # Show environment validation
            print("\n🔍 Validação do ambiente:")
            env_validation = validate_environment()
            for key, value in env_validation.items():
                status = "✓" if value else "✗"
                print(f"  {status} {key}: {value}")
            
            # Show configuration summary
            print("\n⚙️ Resumo da configuração:")
            config_summary = get_configuration_summary()
            print(f"  • Agentes disponíveis: {len(config_summary['available_agents'])}")
            print(f"  • Workflows disponíveis: {len(config_summary['available_workflows'])}")
            print(f"  • Modelo LLM: {config_summary['llm_config']['model']}")
            
        else:
            print("⚠️ CrewAI não está disponível. Verifique a instalação.")
            
    except Exception as e:
        print(f"❌ Erro na demonstração básica: {e}")


def demo_sentiment_analysis_tool():
    """Demonstrate sentiment analysis with CrewAI tools"""
    print("\n" + "=" * 80)
    print("DEMO: Análise de Sentimentos com CrewAI Tools")
    print("=" * 80)
    
    sample_texts = [
        "Art. 1º É livre a manifestação do pensamento, sendo vedado o anonimato.",
        "A violação do disposto neste artigo resultará em multa de 1000 a 10000 reais.",
        "Fica autorizada a criação de programa de incentivo à inovação tecnológica.",
        "É proibido o descarte inadequado de resíduos tóxicos no meio ambiente."
    ]
    
    try:
        from src.modules.nlp import enhanced_sentiment_analysis_tool
        
        for i, text in enumerate(sample_texts, 1):
            print(f"\n📝 Texto {i}: {text}")
            print("🔍 Análise de sentimentos:")
            
            try:
                result = enhanced_sentiment_analysis_tool(text)
                parsed_result = json.loads(result)
                
                if "error" in parsed_result:
                    print(f"  ❌ Erro: {parsed_result['error']}")
                else:
                    basic_sentiment = parsed_result.get("basic_sentiment", {})
                    print(f"  • Classificação: {basic_sentiment.get('classification', 'N/A')}")
                    print(f"  • Polaridade: {basic_sentiment.get('polarity', 0):.3f}")
                    
                    emotions = parsed_result.get("emotions", {})
                    print(f"  • Emoção dominante: {emotions.get('dominant_emotion', 'N/A')}")
                    
                    intensity = parsed_result.get("intensity", {})
                    print(f"  • Intensidade: {intensity.get('intensity', 0):.3f}")
                    print(f"  • Confiança: {intensity.get('confidence', 0):.3f}")
                    
            except Exception as e:
                print(f"  ❌ Erro na análise: {e}")
                
    except ImportError:
        print("⚠️ Ferramentas de análise de sentimentos não disponíveis")
    except Exception as e:
        print(f"❌ Erro na demonstração de sentimentos: {e}")


def demo_legal_classification_tool():
    """Demonstrate legal document classification"""
    print("\n" + "=" * 80)
    print("DEMO: Classificação de Documentos Legais")
    print("=" * 80)
    
    legal_samples = [
        {
            "text": "LEI Nº 12.965, DE 23 DE ABRIL DE 2014. Estabelece princípios, garantias, direitos e deveres para o uso da Internet no Brasil.",
            "type": "subject"
        },
        {
            "text": "Art. 1º Para os efeitos desta lei, considera-se: I - internet: o sistema constituído do conjunto de protocolos lógicos;",
            "type": "article_type"
        },
        {
            "text": "É vedado o fornecimento a terceiros de dados pessoais, salvo mediante consentimento livre, expresso e informado;",
            "type": "legal_intention"
        }
    ]
    
    try:
        from src.modules.nlp import legal_document_classification_tool
        
        for i, sample in enumerate(legal_samples, 1):
            print(f"\n📄 Documento {i}:")
            print(f"   Texto: {sample['text'][:100]}...")
            print(f"   Tipo de classificação: {sample['type']}")
            
            try:
                result = legal_document_classification_tool(sample['text'], sample['type'])
                parsed_result = json.loads(result)
                
                if "error" in parsed_result:
                    print(f"  ❌ Erro: {parsed_result['error']}")
                else:
                    print(f"  🏷️ Resultado: {parsed_result.get('result', 'N/A')}")
                    print(f"  📊 Tipo: {parsed_result.get('classification_type', 'N/A')}")
                    
            except Exception as e:
                print(f"  ❌ Erro na classificação: {e}")
                
    except ImportError:
        print("⚠️ Ferramentas de classificação legal não disponíveis")
    except Exception as e:
        print(f"❌ Erro na demonstração de classificação: {e}")


def demo_comprehensive_analysis():
    """Demonstrate comprehensive legal analysis"""
    print("\n" + "=" * 80)
    print("DEMO: Análise Legal Abrangente")
    print("=" * 80)
    
    comprehensive_sample = """
    LEI Nº 13.709, DE 14 DE AGOSTO DE 2018.
    
    Lei Geral de Proteção de Dados Pessoais (LGPD)
    
    Art. 1º Esta Lei dispõe sobre o tratamento de dados pessoais, inclusive nos meios digitais, 
    por pessoa natural ou por pessoa jurídica de direito público ou privado, com o objetivo de 
    proteger os direitos fundamentais de liberdade e de privacidade e o livre desenvolvimento 
    da personalidade da pessoa natural.
    
    Art. 2º A disciplina da proteção de dados pessoais tem como fundamentos:
    I - o respeito à privacidade;
    II - a autodeterminação informativa;
    III - a liberdade de expressão, de informação, de comunicação e de opinião;
    """
    
    try:
        from src.modules.nlp import comprehensive_legal_analysis_tool
        
        print(f"📋 Analisando documento:")
        print(f"   {comprehensive_sample[:150]}...")
        
        result = comprehensive_legal_analysis_tool(comprehensive_sample)
        parsed_result = json.loads(result)
        
        if "error" in parsed_result:
            print(f"❌ Erro: {parsed_result['error']}")
        else:
            print("\n📊 Resultados da análise abrangente:")
            classifications = parsed_result.get("classifications", {})
            
            for key, value in classifications.items():
                if value:
                    print(f"  • {key.replace('_', ' ').title()}: {value}")
                    
    except ImportError:
        print("⚠️ Ferramenta de análise abrangente não disponível")
    except Exception as e:
        print(f"❌ Erro na demonstração abrangente: {e}")


def demo_pipeline_functionality():
    """Demonstrate CrewAI pipeline functionality"""
    print("\n" + "=" * 80)
    print("DEMO: Pipeline CrewAI para Processamento de Documentos")
    print("=" * 80)
    
    try:
        from src.modules.nlp import get_available_pipelines, create_pipeline_manager
        
        # Show available pipelines
        print("🔄 Pipelines disponíveis:")
        pipelines = get_available_pipelines()
        
        for pipeline_id, pipeline_info in pipelines.items():
            print(f"\n  📋 {pipeline_id}:")
            print(f"     Descrição: {pipeline_info['description']}")
            print(f"     Caso de uso: {pipeline_info['use_case']}")
            
            config = pipeline_info['config']
            print(f"     Tarefas: {len(config['tasks'])}")
            print(f"     Duração estimada: {config['estimated_duration']}s")
            print(f"     Complexidade: {config['complexity']}")
        
        # Demonstrate pipeline manager
        print("\n⚙️ Criando gerenciador de pipeline:")
        manager = create_pipeline_manager()
        
        # Show pipeline statistics (will be empty initially)
        stats = manager.get_pipeline_statistics()
        print(f"   Execuções registradas: {stats.get('total_executions', 0)}")
        
    except ImportError:
        print("⚠️ Funcionalidade de pipeline não disponível")
    except Exception as e:
        print(f"❌ Erro na demonstração de pipeline: {e}")


def demo_text_preprocessing():
    """Demonstrate text preprocessing tool"""
    print("\n" + "=" * 80)
    print("DEMO: Pré-processamento de Texto")
    print("=" * 80)
    
    raw_text = """
    Art.   1º    É  livre    a manifestação  do  pensamento,    sendo   vedado o anonimato!!!  
    
    § 1º   Ninguém   será   obrigado  a   fazer...   
    """
    
    operations = [
        "clean",
        "normalize",
        "clean,normalize",
        "clean,normalize,lowercase"
    ]
    
    try:
        from src.modules.nlp import text_preprocessing_tool
        
        print(f"📝 Texto original:")
        print(f"   '{raw_text}'")
        
        for operation in operations:
            print(f"\n🔧 Operação: {operation}")
            
            try:
                result = text_preprocessing_tool(raw_text, operation)
                parsed_result = json.loads(result)
                
                if "error" in parsed_result:
                    print(f"  ❌ Erro: {parsed_result['error']}")
                else:
                    processed = parsed_result.get("processed_text", "")
                    print(f"  ✓ Resultado: '{processed}'")
                    
            except Exception as e:
                print(f"  ❌ Erro no processamento: {e}")
                
    except ImportError:
        print("⚠️ Ferramenta de pré-processamento não disponível")
    except Exception as e:
        print(f"❌ Erro na demonstração de pré-processamento: {e}")


def demo_backward_compatibility():
    """Demonstrate that existing functionality still works"""
    print("\n" + "=" * 80)
    print("DEMO: Compatibilidade com Funcionalidades Existentes")
    print("=" * 80)
    
    try:
        # Test existing classifier
        from src.modules.nlp import classifier, get_simple_classifier
        
        print("✓ Classificador tradicional disponível")
        print("✓ Classificador simples disponível")
        
        # Test enhanced modules if available
        try:
            from src.modules.nlp import get_classifier, EnhancedSentimentAnalyzer
            print("✓ Classificador aprimorado disponível")
            print("✓ Analisador de sentimentos aprimorado disponível")
        except ImportError:
            print("⚠️ Módulos aprimorados não disponíveis")
        
        # Test sentiment analysis
        try:
            from src.modules.nlp import sentiment_analysis_enhanced
            result = sentiment_analysis_enhanced("Texto de teste para análise de sentimentos.")
            print("✓ Análise de sentimentos tradicional funcionando")
        except (ImportError, Exception) as e:
            print(f"⚠️ Análise de sentimentos tradicional: {e}")
            
    except Exception as e:
        print(f"❌ Erro na verificação de compatibilidade: {e}")


def main():
    """Run all demonstrations"""
    print("🚀 DEMONSTRAÇÃO COMPLETA: Integração CrewAI no Módulo NLP")
    print(f"⏰ Timestamp: {datetime.now().isoformat()}")
    
    try:
        # Run all demos
        demo_basic_crewai_functionality()
        demo_sentiment_analysis_tool()
        demo_legal_classification_tool()
        demo_comprehensive_analysis()
        demo_text_preprocessing()
        demo_pipeline_functionality()
        demo_backward_compatibility()
        
        print("\n" + "=" * 80)
        print("✅ DEMONSTRAÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 80)
        
        print("\n📝 Resumo das funcionalidades demonstradas:")
        print("  • Integração básica do CrewAI")
        print("  • Ferramentas de análise de sentimentos")
        print("  • Classificação de documentos legais")
        print("  • Análise legal abrangente")
        print("  • Pipelines de processamento")
        print("  • Pré-processamento de texto")
        print("  • Compatibilidade com funcionalidades existentes")
        
        print("\n🎯 Próximos passos recomendados:")
        print("  1. Configure variáveis de ambiente para OpenAI/LLM")
        print("  2. Execute testes específicos com dados reais")
        print("  3. Customize agentes e workflows conforme necessário")
        print("  4. Integre com sistemas de produção")
        
    except Exception as e:
        print(f"\n❌ ERRO GERAL NA DEMONSTRAÇÃO: {e}")
        logger.exception("Erro detalhado na demonstração")


if __name__ == "__main__":
    main()