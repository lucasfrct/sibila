# Example Usage: CrewAI NLP Integration
# Shows how to use the new CrewAI-powered NLP capabilities

import sys
import os
import json

# Add project path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def example_sentiment_analysis():
    """Example of sentiment analysis using CrewAI tools"""
    print("🔍 Exemplo: Análise de Sentimentos com CrewAI")
    print("-" * 50)
    
    from src.modules.nlp.crewai_integration import enhanced_sentiment_analysis_tool
    
    legal_texts = [
        "Art. 5º É livre a manifestação do pensamento, sendo vedado o anonimato.",
        "A violação desta norma resultará em multa severa e processo criminal.",
        "Fica autorizada a criação de programa de incentivo à inovação.",
        "É proibido terminantemente o descarte de resíduos tóxicos."
    ]
    
    for i, text in enumerate(legal_texts, 1):
        print(f"\n📄 Texto {i}: {text}")
        result = enhanced_sentiment_analysis_tool._run(text)
        data = json.loads(result)
        
        sentiment = data['basic_sentiment']['classification']
        polarity = data['basic_sentiment']['polarity']
        emotion = data['emotions']['dominant_emotion']
        
        print(f"   Sentimento: {sentiment} (polaridade: {polarity:.3f})")
        print(f"   Emoção dominante: {emotion}")


def example_legal_classification():
    """Example of legal document classification"""
    print("\n⚖️ Exemplo: Classificação de Documentos Legais")
    print("-" * 50)
    
    from src.modules.nlp.crewai_integration import legal_document_classification_tool
    
    documents = [
        {
            "text": "LEI Nº 12.965, DE 23 DE ABRIL DE 2014. Estabelece princípios para uso da Internet.",
            "type": "subject",
            "description": "Marco Civil da Internet"
        },
        {
            "text": "Para os efeitos desta lei, considera-se internet o sistema de protocolos lógicos.",
            "type": "article_type",
            "description": "Artigo de definição"
        }
    ]
    
    for doc in documents:
        print(f"\n📋 {doc['description']}")
        print(f"   Texto: {doc['text'][:80]}...")
        
        result = legal_document_classification_tool._run(doc['text'], doc['type'])
        data = json.loads(result)
        
        if data.get('result'):
            print(f"   Classificação: {data['result']}")
        else:
            print(f"   Status: Modelo em treinamento")


def example_comprehensive_analysis():
    """Example of comprehensive legal analysis"""
    print("\n📊 Exemplo: Análise Legal Abrangente")
    print("-" * 50)
    
    from src.modules.nlp.crewai_integration import comprehensive_legal_analysis_tool
    
    comprehensive_text = """
    Art. 1º Esta Lei estabelece princípios, garantias, direitos e deveres para o uso da internet 
    no Brasil e determina as diretrizes para atuação da União, dos Estados, do Distrito Federal 
    e dos Municípios em relação à matéria.
    
    Art. 2º A disciplina do uso da internet no Brasil tem como fundamento o respeito à 
    liberdade de expressão, bem como:
    I - o reconhecimento da escala mundial da rede;
    II - os direitos humanos, o desenvolvimento da personalidade e o exercício da cidadania em meios digitais.
    """
    
    print("📄 Analisando documento legal completo...")
    result = comprehensive_legal_analysis_tool._run(comprehensive_text)
    data = json.loads(result)
    
    classifications = data.get('classifications', {})
    print("\n🏷️ Classificações identificadas:")
    
    for key, value in classifications.items():
        if value:
            label = key.replace('_', ' ').title()
            print(f"   • {label}: {value}")


def example_text_preprocessing():
    """Example of text preprocessing"""
    print("\n🔧 Exemplo: Pré-processamento de Texto")
    print("-" * 50)
    
    from src.modules.nlp.crewai_integration import text_preprocessing_tool
    
    messy_text = """
    Art.  1º    É    LIVRE   a   manifestação    do  pensamento,    sendo   vedado   o   anonimato!!!
    
    §  1º   -   Ninguém   será    obrigado...   
    """
    
    operations = ["clean", "normalize", "clean,normalize", "clean,normalize,lowercase"]
    
    print(f"📝 Texto original: '{messy_text.strip()}'")
    
    for operation in operations:
        result = text_preprocessing_tool._run(messy_text, operation)
        data = json.loads(result)
        processed = data['processed_text']
        print(f"\n🔧 {operation}: '{processed}'")


def example_pipeline_overview():
    """Example showing available pipelines"""
    print("\n🔄 Exemplo: Pipelines Disponíveis")
    print("-" * 50)
    
    from src.modules.nlp import get_available_pipelines
    
    pipelines = get_available_pipelines()
    
    for pipeline_id, info in pipelines.items():
        print(f"\n📋 {pipeline_id}")
        print(f"   Descrição: {info['description']}")
        print(f"   Caso de uso: {info['use_case']}")
        
        config = info['config']
        print(f"   Detalhes:")
        print(f"     • Tarefas: {len(config['tasks'])}")
        print(f"     • Duração estimada: {config['estimated_duration']}s")
        print(f"     • Complexidade: {config['complexity']}")


def main():
    """Run all examples"""
    print("🚀 EXEMPLOS DE USO: CrewAI NLP Integration")
    print("=" * 70)
    
    try:
        # Suppress warnings for cleaner output
        import warnings
        warnings.filterwarnings("ignore")
        
        example_sentiment_analysis()
        example_legal_classification()
        example_comprehensive_analysis()
        example_text_preprocessing()
        example_pipeline_overview()
        
        print("\n" + "=" * 70)
        print("✅ TODOS OS EXEMPLOS EXECUTADOS COM SUCESSO!")
        print("\n💡 Próximos passos:")
        print("  1. Configure OpenAI API key para usar agentes LLM")
        print("  2. Execute workflows completos com CrewAI")
        print("  3. Personalize agentes para seu domínio específico")
        print("  4. Integre com seus sistemas de produção")
        
    except Exception as e:
        print(f"\n❌ Erro na execução dos exemplos: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()