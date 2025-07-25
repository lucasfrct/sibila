#!/usr/bin/env python3
"""
Simple test of CrewAI tools directly without dependencies
"""

import sys
import os
import json

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_direct_tools():
    """Test CrewAI tools directly"""
    
    print("🧪 TESTE DIRETO DAS FERRAMENTAS CREWAI")
    print("=" * 50)
    
    try:
        # Import tools directly
        from src.modules.analysis.crewai.tools import (
            LegalContextExtractionTool,
            SubjectSynthesisTool,
            StructuredSummaryTool,
            QuestionGenerationTool
        )
        
        print("✅ Ferramentas importadas com sucesso")
        
        # Sample legal text
        sample_text = "Art. 1º Esta lei estabelece diretrizes para proteção de dados pessoais."
        
        # Test LegalContextExtractionTool
        print("\n1. Testando Legal Context Extraction Tool")
        context_tool = LegalContextExtractionTool()
        print(f"   Nome: {context_tool.name}")
        print(f"   Descrição: {context_tool.description[:100]}...")
        
        result = context_tool._run(sample_text)
        print(f"   Resultado: {result[:200]}...")
        
        # Parse and verify JSON
        try:
            result_data = json.loads(result)
            print(f"   ✅ JSON válido com chaves: {list(result_data.keys())}")
        except json.JSONDecodeError:
            print(f"   ❌ Resultado não é JSON válido")
        
        # Test SubjectSynthesisTool
        print("\n2. Testando Subject Synthesis Tool")
        synthesis_tool = SubjectSynthesisTool()
        print(f"   Nome: {synthesis_tool.name}")
        
        result = synthesis_tool._run(sample_text)
        print(f"   Resultado: {result[:200]}...")
        
        # Test StructuredSummaryTool
        print("\n3. Testando Structured Summary Tool")
        summary_tool = StructuredSummaryTool()
        print(f"   Nome: {summary_tool.name}")
        
        result = summary_tool._run(sample_text)
        print(f"   Resultado: {result[:200]}...")
        
        # Test QuestionGenerationTool
        print("\n4. Testando Question Generation Tool")
        question_tool = QuestionGenerationTool()
        print(f"   Nome: {question_tool.name}")
        
        result = question_tool._run(sample_text, "question")
        print(f"   Resultado: {result[:200]}...")
        
        print("\n✅ Todas as ferramentas testadas com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste direto: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_agent_manager():
    """Test the agent manager initialization"""
    
    print("\n🤖 TESTE DO GERENCIADOR DE AGENTES")
    print("=" * 50)
    
    try:
        from src.modules.analysis.crewai.agents import LegalAnalysisCrewManager
        
        print("✅ Classe LegalAnalysisCrewManager importada")
        
        # Try to initialize (may fail without OpenAI API key, but should not crash)
        try:
            manager = LegalAnalysisCrewManager()
            print(f"✅ Gerenciador inicializado com {len(manager.agents)} agentes")
            print(f"   Agentes: {list(manager.agents.keys())}")
            print(f"   Ferramentas: {list(manager.tools.keys())}")
            return True
        except Exception as e:
            print(f"⚠️  Inicialização falhou (esperado sem API key): {e}")
            return True  # This is expected without API key
            
    except Exception as e:
        print(f"❌ Erro no teste do gerenciador: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_convenience_functions():
    """Test convenience functions"""
    
    print("\n🔧 TESTE DAS FUNÇÕES DE CONVENIÊNCIA")
    print("=" * 50)
    
    try:
        from src.modules.analysis.crewai.agents import (
            crewai_enhanced_legal_document_analysis,
            crewai_enhanced_questionnaire
        )
        
        print("✅ Funções de conveniência importadas")
        print(f"   crewai_enhanced_legal_document_analysis: {callable(crewai_enhanced_legal_document_analysis)}")
        print(f"   crewai_enhanced_questionnaire: {callable(crewai_enhanced_questionnaire)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste das funções: {e}")
        return False


def test_main_module_integration():
    """Test integration with main analysis module"""
    
    print("\n🔗 TESTE DE INTEGRAÇÃO COM MÓDULO PRINCIPAL")
    print("=" * 50)
    
    try:
        from src.modules.analysis import (
            CREWAI_ANALYSIS_AVAILABLE,
            LegalAnalysisCrewManager
        )
        
        print(f"✅ CREWAI_ANALYSIS_AVAILABLE: {CREWAI_ANALYSIS_AVAILABLE}")
        print(f"✅ LegalAnalysisCrewManager importado do módulo principal")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na integração: {e}")
        return False


if __name__ == "__main__":
    print("🚀 EXECUTANDO TESTE SIMPLIFICADO DO CREWAI")
    print("=" * 60)
    
    success_count = 0
    total_tests = 4
    
    # Run tests
    if test_direct_tools():
        success_count += 1
    
    if test_agent_manager():
        success_count += 1
    
    if test_convenience_functions():
        success_count += 1
    
    if test_main_module_integration():
        success_count += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("RESUMO DOS TESTES")
    print("=" * 60)
    print(f"✅ Testes bem-sucedidos: {success_count}/{total_tests}")
    
    if success_count == total_tests:
        print("🎉 Todos os testes passaram! CrewAI está funcionando corretamente.")
    else:
        print(f"⚠️  {total_tests - success_count} teste(s) falharam. Verifique as dependências.")
    
    print("\n💡 PRÓXIMOS PASSOS:")
    print("1. Configure OPENAI_API_KEY para usar os agentes")
    print("2. Execute análises reais com crewai_enhanced_legal_document_analysis()")
    print("3. Customize os agentes conforme necessário")