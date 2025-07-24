#!/usr/bin/env python3
"""
Demonstration of CrewAI Integration for Legal Analysis

This script demonstrates how the new CrewAI-based analysis system works,
replacing the traditional direct LLM approach with specialized agents.
"""

import os
import sys
import json
from typing import Dict, Any

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def demo_crewai_legal_analysis():
    """Demonstrate CrewAI legal analysis functionality"""
    
    print("=" * 80)
    print("DEMONSTRAÇÃO: ANÁLISE JURÍDICA COM CREWAI")
    print("=" * 80)
    
    # Sample legal document for demonstration
    sample_legal_text = """
    Lei nº 12.345/2023
    
    Art. 1º Esta lei estabelece diretrizes para a proteção de dados pessoais no âmbito 
    da administração pública federal, visando garantir a privacidade dos cidadãos.
    
    Art. 2º Para os fins desta lei, considera-se:
    I - dado pessoal: informação relacionada a pessoa natural identificada ou identificável;
    II - tratamento: toda operação realizada com dados pessoais;
    III - consentimento: manifestação livre, informada e inequívoca.
    
    Art. 3º O tratamento de dados pessoais observará os seguintes princípios:
    I - finalidade: realização do tratamento para propósitos legítimos;
    II - adequação: compatibilidade do tratamento com as finalidades;
    III - necessidade: limitação ao mínimo necessário.
    
    Art. 4º São direitos dos titulares de dados:
    I - confirmação da existência de tratamento;
    II - acesso aos dados;
    III - correção de dados incompletos;
    IV - anonimização, bloqueio ou eliminação.
    
    Art. 5º O descumprimento das disposições desta lei sujeita o infrator às seguintes sanções:
    I - advertência;
    II - multa simples de até R$ 50.000.000,00;
    III - suspensão parcial do funcionamento.
    """
    
    try:
        # Import CrewAI components
        from src.modules.analysis import (
            CREWAI_ANALYSIS_AVAILABLE,
            LegalAnalysisCrewManager,
            crewai_enhanced_legal_document_analysis
        )
        
        if not CREWAI_ANALYSIS_AVAILABLE:
            print("❌ CrewAI analysis não está disponível")
            print("Verifique se o CrewAI está instalado e configurado corretamente")
            return
        
        print("✅ CrewAI analysis disponível")
        print("\n1. CONFIGURAÇÃO DOS AGENTES")
        print("-" * 40)
        
        # Note: In a real scenario, you would set OPENAI_API_KEY environment variable
        # For demonstration, we'll show the setup process
        print("⚠️  ATENÇÃO: Para usar o CrewAI, configure a variável OPENAI_API_KEY")
        print("   export OPENAI_API_KEY='sua-chave-da-openai'")
        
        # Check if API key is available
        openai_key = os.getenv('OPENAI_API_KEY')
        if not openai_key:
            print("📝 Demonstração em modo simulado (sem chave da OpenAI)")
            demo_without_api_key(sample_legal_text)
            return
        
        print("🔑 Chave da OpenAI detectada - executando análise real")
        demo_with_api_key(sample_legal_text, openai_key)
        
    except ImportError as e:
        print(f"❌ Erro na importação: {e}")
        print("Verifique se todas as dependências estão instaladas")
    except Exception as e:
        print(f"❌ Erro na demonstração: {e}")


def demo_without_api_key(legal_text: str):
    """Demonstrate CrewAI setup without actually calling the API"""
    
    print("\n2. ESTRUTURA DOS AGENTES CREWAI")
    print("-" * 40)
    
    agent_descriptions = {
        "context_analyst": {
            "role": "Legal Context Analyst",
            "goal": "Extrair contexto jurídico abrangente",
            "tools": ["LegalContextExtractionTool", "ConstitutionalRetrievalTool"]
        },
        "subject_expert": {
            "role": "Legal Subject Matter Expert", 
            "goal": "Analisar e sintetizar o assunto jurídico principal",
            "tools": ["SubjectSynthesisTool", "StructuredSummaryTool"]
        },
        "structure_analyst": {
            "role": "Legal Document Structure Analyst",
            "goal": "Analisar estrutura e artigos individuais",
            "tools": ["DocumentArticleAnalysisTool"]
        },
        "legal_examiner": {
            "role": "Legal Examiner and Question Generator",
            "goal": "Gerar perguntas e conduzir exames jurídicos",
            "tools": ["QuestionGenerationTool", "QuestionAnsweringTool"]
        },
        "assessment_coordinator": {
            "role": "Senior Legal Assessment Coordinator",
            "goal": "Coordenar análise abrangente e fornecer avaliação geral",
            "tools": ["LegalAssessmentTool"]
        }
    }
    
    for agent_id, agent_info in agent_descriptions.items():
        print(f"\n🤖 {agent_info['role']}")
        print(f"   Objetivo: {agent_info['goal']}")
        print(f"   Ferramentas: {', '.join(agent_info['tools'])}")
    
    print("\n3. FERRAMENTAS DISPONÍVEIS")
    print("-" * 40)
    
    tools_descriptions = {
        "LegalContextExtractionTool": "Extrai entidades, ações, deduções e pontos críticos",
        "SubjectSynthesisTool": "Gera síntese objetiva do assunto jurídico principal",
        "StructuredSummaryTool": "Cria resumos estruturados organizados por seções",
        "DocumentArticleAnalysisTool": "Analisa artigos individuais com detalhamento",
        "QuestionGenerationTool": "Gera perguntas jurídicas e questionários",
        "LegalAssessmentTool": "Fornece avaliação jurídica abrangente",
        "ConstitutionalRetrievalTool": "Recupera informações constitucionais relevantes",
        "QuestionAnsweringTool": "Responde perguntas baseadas em documentos"
    }
    
    for tool_name, description in tools_descriptions.items():
        print(f"🔧 {tool_name}")
        print(f"   {description}")
    
    print("\n4. FLUXO DE ANÁLISE SEQUENCIAL")
    print("-" * 40)
    
    workflow_steps = [
        "1. Context Analyst → Extrai contexto jurídico estruturado",
        "2. Subject Expert → Gera síntese e resumo estruturado", 
        "3. Structure Analyst → Analisa artigos e estrutura do documento",
        "4. Legal Examiner → Cria perguntas e material de exame",
        "5. Assessment Coordinator → Integra todas as análises em avaliação final"
    ]
    
    for step in workflow_steps:
        print(f"📋 {step}")
    
    print("\n5. COMPARAÇÃO: ANTES vs DEPOIS")
    print("-" * 40)
    
    comparison = {
        "ANTES (LLM Direto)": [
            "❌ Chamadas diretas ao modelo Ollama",
            "❌ Funções isoladas sem coordenação",
            "❌ Sem especialização por domínio",
            "❌ Processamento sequencial simples",
            "❌ Limitado a um único modelo local"
        ],
        "DEPOIS (CrewAI)": [
            "✅ Agentes especializados por área jurídica",
            "✅ Coordenação inteligente entre agentes",
            "✅ Ferramentas reutilizáveis e modulares",
            "✅ Processamento colaborativo",
            "✅ Integração com modelos OpenAI (GPT-3.5/4)"
        ]
    }
    
    for approach, features in comparison.items():
        print(f"\n{approach}:")
        for feature in features:
            print(f"  {feature}")
    
    print("\n6. EXEMPLO DE USO")
    print("-" * 40)
    
    usage_example = '''
# Uso tradicional (substituído)
from src.modules.analysis import enhanced_legal_document_analysis
resultado = enhanced_legal_document_analysis(texto_juridico)

# Novo uso com CrewAI
from src.modules.analysis import crewai_enhanced_legal_document_analysis
resultado = crewai_enhanced_legal_document_analysis(
    document_text=texto_juridico,
    openai_api_key="sua-chave-api"
)

# Uso direto do gerenciador de agentes
from src.modules.analysis import LegalAnalysisCrewManager
manager = LegalAnalysisCrewManager(openai_api_key="sua-chave-api")
analise = manager.analyze_legal_document(texto_juridico)
'''
    
    print(usage_example)


def demo_with_api_key(legal_text: str, api_key: str):
    """Demonstrate actual CrewAI analysis with API key"""
    
    print("\n2. EXECUTANDO ANÁLISE REAL COM CREWAI")
    print("-" * 40)
    
    try:
        from src.modules.analysis import LegalAnalysisCrewManager
        
        # Initialize the crew manager
        print("🚀 Inicializando gerenciador de agentes...")
        manager = LegalAnalysisCrewManager(openai_api_key=api_key, model_name="gpt-3.5-turbo")
        
        print("✅ Agentes inicializados com sucesso")
        print("📄 Analisando documento jurídico...")
        
        # Perform the analysis
        result = manager.analyze_legal_document(legal_text)
        
        print("\n3. RESULTADOS DA ANÁLISE")
        print("-" * 40)
        
        if result.get("success"):
            print("✅ Análise concluída com sucesso")
            print(f"🤖 Modelo usado: {result.get('model_used')}")
            print(f"👥 Agentes envolvidos: {', '.join(result.get('agents_involved', []))}")
            print(f"🔧 Ferramentas utilizadas: {', '.join(result.get('tools_used', []))}")
            
            print(f"\n📋 ANÁLISE ABRANGENTE:")
            print("=" * 60)
            print(result.get('comprehensive_analysis', 'Não disponível'))
            
            if 'structured_analysis' in result:
                print(f"\n📊 ANÁLISE ESTRUTURADA:")
                print("=" * 60)
                print(json.dumps(result['structured_analysis'], indent=2, ensure_ascii=False))
        else:
            print(f"❌ Erro na análise: {result.get('error')}")
    
    except Exception as e:
        print(f"❌ Erro durante execução: {e}")
        print("💡 Verifique se a chave da OpenAI está correta e tem créditos disponíveis")


def demo_individual_tools():
    """Demonstrate individual tool usage"""
    
    print("\n" + "=" * 80)
    print("DEMONSTRAÇÃO: USO INDIVIDUAL DAS FERRAMENTAS")
    print("=" * 80)
    
    try:
        from src.modules.analysis.crewai.tools import (
            LegalContextExtractionTool,
            SubjectSynthesisTool,
            QuestionGenerationTool
        )
        
        # Sample text for tool demonstration
        sample_text = "Art. 1º Esta lei estabelece diretrizes para proteção de dados pessoais."
        
        print("\n1. FERRAMENTA DE EXTRAÇÃO DE CONTEXTO")
        print("-" * 50)
        
        context_tool = LegalContextExtractionTool()
        print(f"🔧 Nome: {context_tool.name}")
        print(f"📝 Descrição: {context_tool.description[:100]}...")
        
        # Note: In a real scenario with API key, you could run:
        # result = context_tool._run(sample_text)
        # print(f"📊 Resultado: {result}")
        
        print("\n2. FERRAMENTA DE SÍNTESE DE ASSUNTO")
        print("-" * 50)
        
        synthesis_tool = SubjectSynthesisTool()
        print(f"🔧 Nome: {synthesis_tool.name}")
        print(f"📝 Descrição: {synthesis_tool.description[:100]}...")
        
        print("\n3. FERRAMENTA DE GERAÇÃO DE PERGUNTAS")
        print("-" * 50)
        
        question_tool = QuestionGenerationTool()
        print(f"🔧 Nome: {question_tool.name}")
        print(f"📝 Descrição: {question_tool.description[:100]}...")
        
        print("\n✅ Todas as ferramentas carregadas com sucesso")
        print("💡 Para execução real, configure OPENAI_API_KEY e use os agentes")
        
    except ImportError as e:
        print(f"❌ Erro na importação das ferramentas: {e}")


if __name__ == "__main__":
    print("🚀 Iniciando demonstração da integração CrewAI...")
    
    # Main demonstration
    demo_crewai_legal_analysis()
    
    # Individual tools demonstration
    demo_individual_tools()
    
    print("\n" + "=" * 80)
    print("PRÓXIMOS PASSOS")
    print("=" * 80)
    print("1. Configure sua chave da OpenAI: export OPENAI_API_KEY='sua-chave'")
    print("2. Execute: python demo_crewai_legal_analysis.py")
    print("3. Integre no seu sistema usando as novas funções CrewAI")
    print("4. Customize os agentes conforme suas necessidades específicas")
    print("\n✨ Transformação para CrewAI concluída com sucesso!")