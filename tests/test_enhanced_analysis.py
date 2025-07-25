#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Teste da funcionalidade de análise jurídica aprimorada.

Este script testa a integração do módulo de análise com os serviços
de documento e catálogo, focando na análise jurídica abrangente.
"""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_service_integration():
    """Testa a verificação de integração com serviços"""
    print("=" * 60)
    print("TESTE: Verificação de Integração de Serviços")
    print("=" * 60)
    
    try:
        from src.modules.analysis.enhanced_legal_analysis import check_service_integration
        
        status = check_service_integration()
        print("Status dos serviços:")
        for service, available in status.items():
            status_text = "✓ Disponível" if available else "✗ Não disponível"
            print(f"  {service}: {status_text}")
        
        return True
    except Exception as e:
        print(f"Erro no teste de integração: {e}")
        return False

def test_legal_context_extraction():
    """Testa a extração de contexto jurídico"""
    print("\n" + "=" * 60)
    print("TESTE: Extração de Contexto Jurídico")
    print("=" * 60)
    
    try:
        from src.modules.analysis.enhanced_legal_analysis import extract_legal_context
        
        # Texto jurídico de exemplo
        sample_text = """
        Art. 5º Todos são iguais perante a lei, sem distinção de qualquer natureza,
        garantindo-se aos brasileiros e aos estrangeiros residentes no País a 
        inviolabilidade do direito à vida, à liberdade, à igualdade, à segurança
        e à propriedade, nos termos seguintes:
        
        I - homens e mulheres são iguais em direitos e obrigações;
        II - ninguém será obrigado a fazer ou deixar de fazer alguma coisa 
        senão em virtude de lei;
        
        § 1º A aplicação desta lei será realizada no prazo de 30 dias.
        § 2º O descumprimento desta norma resultará em multa de R$ 1.000,00.
        """
        
        print("Texto de exemplo para análise:")
        print(sample_text[:200] + "...")
        
        context = extract_legal_context(sample_text)
        
        print(f"\nContexto extraído:")
        print(f"  Nomes/Entidades: {len(context.names)} identificados")
        print(f"  Ações: {len(context.actions)} identificadas")
        print(f"  Pontos de atenção: {len(context.attention_points)} identificados")
        print(f"  Termos jurídicos: {len(context.legal_terms)} identificados")
        print(f"  Datas/Prazos: {len(context.dates_deadlines)} identificados")
        print(f"  Penalidades: {len(context.penalties)} identificadas")
        
        return True
    except Exception as e:
        print(f"Erro no teste de extração de contexto: {e}")
        return False

def test_synthesis_generation():
    """Testa a geração de síntese jurídica"""
    print("\n" + "=" * 60)
    print("TESTE: Geração de Síntese")
    print("=" * 60)
    
    try:
        from src.modules.analysis.enhanced_legal_analysis import (
            generate_subject_synthesis,
            generate_structured_summary
        )
        
        sample_text = """
        Lei nº 12.527, de 18 de novembro de 2011
        Regula o acesso a informações previsto no inciso XXXIII do art. 5º, 
        no inciso II do § 3º do art. 37 e no § 2º do art. 216 da Constituição Federal.
        
        Art. 1º Esta Lei dispõe sobre os procedimentos a serem observados pela União, 
        Estados, Distrito Federal e Municípios, com o fim de garantir o acesso a informações.
        
        Art. 2º Aplicam-se as disposições desta Lei, no que couber:
        I - aos órgãos públicos integrantes da administração direta;
        II - às autarquias, às fundações públicas, às empresas públicas.
        """
        
        print("Gerando síntese do assunto...")
        synthesis = generate_subject_synthesis(sample_text)
        print(f"Síntese: {synthesis}")
        
        print("\nGerando resumo estruturado...")
        summary = generate_structured_summary(sample_text)
        print(f"Resumo estruturado: {summary[:200]}...")
        
        return True
    except Exception as e:
        print(f"Erro no teste de síntese: {e}")
        return False

def test_enhanced_analysis():
    """Testa a análise jurídica abrangente"""
    print("\n" + "=" * 60)
    print("TESTE: Análise Jurídica Abrangente")
    print("=" * 60)
    
    try:
        from src.modules.analysis.enhanced_legal_analysis import (
            enhanced_legal_document_analysis,
            format_synthesis_report
        )
        
        sample_legal_document = """
        DECRETO Nº 10.139, DE 28 DE NOVEMBRO DE 2019
        
        Dispõe sobre a revisão e a consolidação dos atos normativos inferiores a decreto.
        
        O PRESIDENTE DA REPÚBLICA, no uso da atribuição que lhe confere o art. 84, 
        caput, inciso IV, da Constituição Federal, e tendo em vista o disposto na 
        Lei Complementar nº 95, de 26 de fevereiro de 1998,
        
        DECRETA:
        
        Art. 1º Os Ministérios e órgãos da Presidência da República procederão à 
        revisão e à consolidação dos atos normativos que editaram.
        
        § 1º A revisão e a consolidação de que trata o caput serão realizadas no 
        prazo de dois anos, contado da data de publicação deste Decreto.
        
        § 2º O descumprimento do prazo estabelecido no § 1º implicará 
        responsabilização do agente público competente.
        
        Art. 2º Na revisão dos atos normativos, deverão ser observados os seguintes critérios:
        I - necessidade e adequação da norma para o atendimento do interesse público;
        II - eficácia da norma para o alcance dos objetivos pretendidos;
        III - eficiência na utilização dos recursos disponíveis.
        
        Art. 3º Este Decreto entra em vigor na data de sua publicação.
        
        Brasília, 28 de novembro de 2019; 198º da Independência e 131º da República.
        JAIR MESSIAS BOLSONARO
        """
        
        print("Executando análise jurídica abrangente...")
        print("Texto do documento:")
        print(sample_legal_document[:300] + "...")
        
        # Executar análise completa
        analysis_result = enhanced_legal_document_analysis(sample_legal_document)
        
        print(f"\nResultado da análise:")
        print(f"  Síntese do assunto: {analysis_result.subject_synthesis[:100]}...")
        print(f"  Tipo normativo: {analysis_result.normative_type}")
        print(f"  Categorias: {', '.join(analysis_result.categories) if analysis_result.categories else 'Nenhuma'}")
        print(f"  Artigos analisados: {len(analysis_result.articles_analysis)}")
        print(f"  Entidades no contexto: {len(analysis_result.context.names)}")
        
        # Gerar relatório formatado
        print("\nGerando relatório formatado...")
        report = format_synthesis_report(analysis_result)
        print("Relatório gerado com sucesso!")
        print(f"Tamanho do relatório: {len(report)} caracteres")
        
        return True
    except Exception as e:
        print(f"Erro no teste de análise abrangente: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_import_functionality():
    """Testa se as importações do módulo funcionam corretamente"""
    print("\n" + "=" * 60)
    print("TESTE: Importação de Funcionalidades")
    print("=" * 60)
    
    try:
        # Teste de importação direta
        from src.modules.analysis import enhanced_legal_analysis
        print("✓ Importação do módulo enhanced_legal_analysis bem-sucedida")
        
        # Teste de importação via __init__
        from src.modules.analysis import (
            enhanced_legal_document_analysis,
            check_service_integration,
            ENHANCED_ANALYSIS_AVAILABLE
        )
        print("✓ Importação via __init__.py bem-sucedida")
        print(f"✓ Enhanced analysis disponível: {ENHANCED_ANALYSIS_AVAILABLE}")
        
        return True
    except Exception as e:
        print(f"✗ Erro na importação: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("TESTE DO MÓDULO DE ANÁLISE JURÍDICA APRIMORADA")
    print("=" * 80)
    
    tests = [
        ("Importação", test_import_functionality),
        ("Integração de Serviços", test_service_integration),
        ("Extração de Contexto", test_legal_context_extraction),
        ("Geração de Síntese", test_synthesis_generation),
        ("Análise Abrangente", test_enhanced_analysis)
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"Erro fatal no teste {test_name}: {e}")
            results[test_name] = False
    
    # Resumo dos resultados
    print("\n" + "=" * 80)
    print("RESUMO DOS TESTES")
    print("=" * 80)
    
    for test_name, success in results.items():
        status = "✓ PASSOU" if success else "✗ FALHOU"
        print(f"{test_name}: {status}")
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    
    print(f"\nTotal: {passed_tests}/{total_tests} testes passaram")
    
    if passed_tests == total_tests:
        print("🎉 Todos os testes passaram!")
        return 0
    else:
        print("⚠️  Alguns testes falharam")
        return 1

if __name__ == "__main__":
    sys.exit(main())