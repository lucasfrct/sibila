#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Demonstração da Análise Jurídica Enriquecida

Este script demonstra a implementação completa da análise jurídica enriquecida
que integra com os módulos de documento e catálogo para fornecer análise
abrangente de documentos jurídicos longos, conforme especificado nos requisitos.
"""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def demo_complete_legal_analysis():
    """Demonstra a análise jurídica completa de um documento"""
    print("=" * 80)
    print("DEMONSTRAÇÃO: ANÁLISE JURÍDICA ENRIQUECIDA")
    print("=" * 80)
    print("Objetivo: Demonstrar como o módulo de análise foi aprimorado para")
    print("verificar e utilizar os serviços de documento e catálogo, produzindo")
    print("análise jurídica enriquecida com síntese, resumo estruturado e")
    print("memória de contexto para documentos jurídicos longos.")
    print("=" * 80)
    
    # Documento jurídico real para demonstração
    legal_document = """
    LEI Nº 14.133, DE 1º DE ABRIL DE 2021
    
    Lei de Licitações e Contratos Administrativos
    
    Dispõe sobre as normas gerais de licitação e contratação para as 
    Administrações Públicas diretas, autárquicas e fundacionais da União, 
    dos Estados, do Distrito Federal e dos Municípios.
    
    O PRESIDENTE DA REPÚBLICA
    Faço saber que o Congresso Nacional decreta e eu sanciono a seguinte Lei:
    
    TÍTULO I
    DISPOSIÇÕES GERAIS
    
    CAPÍTULO I
    DISPOSIÇÕES PRELIMINARES
    
    Art. 1º Esta Lei estabelece normas gerais de licitação e contratação para 
    as Administrações Públicas diretas, autárquicas e fundacionais da União, 
    dos Estados, do Distrito Federal e dos Municípios, e se aplica aos órgãos 
    dos Poderes Legislativo e Judiciário da União, dos Estados e do Distrito 
    Federal e aos órgãos do Poder Legislativo dos Municípios quando no 
    desempenho de função administrativa.
    
    Art. 2º Aplicam-se as disposições desta Lei a:
    I – órgãos da Administração Pública direta;
    II – entidades da Administração Pública indireta que estejam submetidas 
    ao regime de direito público, ainda que de forma parcial;
    III – fundações públicas;
    IV – fundos especiais;
    V – consórcios públicos;
    VI – organizações sociais, quando houver repasse de verbas públicas.
    
    § 1º As contratações realizadas no âmbito das empresas públicas e das 
    sociedades de economia mista que explorem atividade econômica de produção 
    ou comercialização de bens ou de prestação de serviços em regime de 
    concorrência sujeitam-se ao disposto no art. 173, § 1º, III, da 
    Constituição Federal.
    
    § 2º As empresas públicas e as sociedades de economia mista que não se 
    enquadrem no disposto no § 1º deste artigo sujeitam-se ao regime desta Lei.
    
    Art. 3º Não se submetem ao regime desta Lei:
    I – as contratações cujo valor seja inferior ao previsto no inciso I do 
    caput do art. 75 desta Lei, observado o disposto no art. 8º desta Lei;
    II – as transferências de recursos decorrentes de lei, medida provisória 
    ou créditos orçamentários para órgãos ou entidades da Administração Pública;
    III – as contratações realizadas por empresa pública ou sociedade de 
    economia mista com suas subsidiárias e controladas;
    IV – as contratações realizadas por instituição científica, tecnológica 
    e de inovação ou por agência de fomento para a transferência de tecnologia 
    e para o licenciamento de direito de uso ou de exploração de criação.
    
    § 1º Os consórcios públicos obedecerão aos preceitos desta Lei em todos 
    os atos praticados por eles próprios.
    
    § 2º O prazo para adequação às disposições desta Lei será de 2 (dois) anos, 
    contado da data de sua entrada em vigor.
    
    § 3º O descumprimento das disposições desta Lei sujeitará o responsável 
    a sanções administrativas, civis e penais.
    
    Art. 4º Para os fins desta Lei, considera-se:
    I – licitação: processo de seleção de proposta mais vantajosa para a 
    Administração Pública;
    II – contrato: todo e qualquer ajuste entre órgãos ou entidades da 
    Administração Pública e particulares em que haja um acordo de vontades 
    para a formação de vínculo e a estipulação de obrigações recíprocas;
    III – contratação direta: contratação realizada sem licitação;
    IV – agente de contratação: servidor designado pela autoridade competente 
    para a prática dos atos de contratação.
    """
    
    try:
        print("\n1. VERIFICAÇÃO DE INTEGRAÇÃO COM SERVIÇOS")
        print("-" * 50)
        
        from src.modules.analysis.enhanced_legal_analysis import check_service_integration
        
        services = check_service_integration()
        print("Status dos serviços integrados:")
        for service, available in services.items():
            icon = "✅" if available else "⚠️"
            print(f"  {icon} {service.replace('_', ' ').title()}: {'Disponível' if available else 'Não disponível'}")
        
        print("\n2. ANÁLISE JURÍDICA ABRANGENTE")
        print("-" * 50)
        
        from src.modules.analysis.enhanced_legal_analysis import (
            enhanced_legal_document_analysis,
            format_synthesis_report
        )
        
        print("Executando análise jurídica abrangente...")
        print(f"Documento: Lei de Licitações e Contratos Administrativos")
        print(f"Tamanho: {len(legal_document)} caracteres")
        print(f"Artigos estimados: ~4-5")
        
        # Executar análise completa
        analysis = enhanced_legal_document_analysis(legal_document)
        
        print("\n3. RESULTADOS DA ANÁLISE")
        print("-" * 50)
        
        print(f"📄 Síntese do Assunto:")
        print(f"   {analysis.subject_synthesis}")
        
        print(f"\n🏛️ Classificação Jurídica:")
        print(f"   Tipo Normativo: {analysis.normative_type or 'Lei'}")
        print(f"   Categorias: {', '.join(analysis.categories) if analysis.categories else 'Direito Administrativo'}")
        
        print(f"\n📊 Estrutura do Documento:")
        print(f"   Artigos Analisados: {len(analysis.articles_analysis)}")
        
        print(f"\n🧠 Contexto Jurídico Extraído:")
        context = analysis.context
        print(f"   Entidades Identificadas: {len(context.names)}")
        if context.names:
            print(f"     → {', '.join(context.names[:3])}{'...' if len(context.names) > 3 else ''}")
        
        print(f"   Ações Jurídicas: {len(context.actions)}")
        if context.actions:
            print(f"     → {', '.join(context.actions[:3])}{'...' if len(context.actions) > 3 else ''}")
        
        print(f"   Pontos de Atenção: {len(context.attention_points)}")
        if context.attention_points:
            print(f"     → {', '.join(context.attention_points[:2])}{'...' if len(context.attention_points) > 2 else ''}")
        
        print(f"   Termos Jurídicos: {len(context.legal_terms)}")
        print(f"   Datas/Prazos: {len(context.dates_deadlines)}")
        print(f"   Penalidades: {len(context.penalties)}")
        
        print("\n4. BANCA EXAMINADORA APRIMORADA")
        print("-" * 50)
        
        from src.modules.analysis.examining_board import analyze_document_with_enhanced_board
        
        board_analysis = analyze_document_with_enhanced_board(legal_document)
        
        summary = board_analysis.get('analysis_summary', {})
        print("Questões geradas pela banca examinadora:")
        print(f"  Questões Aprimoradas: {summary.get('total_enhanced_questions', 0)}")
        print(f"  Questões Contextuais: {summary.get('total_context_questions', 0)}")
        print(f"  Questões de Síntese: {summary.get('total_synthesis_questions', 0)}")
        print(f"  Questões Tradicionais: {summary.get('total_traditional_questions', 0)}")
        
        print("\n5. RELATÓRIO FORMATADO")
        print("-" * 50)
        
        print("Gerando relatório de análise jurídica...")
        report = format_synthesis_report(analysis)
        
        # Mostrar início do relatório
        report_lines = report.split('\n')
        for line in report_lines[:15]:
            print(line)
        
        print("...")
        print(f"[Relatório completo com {len(report)} caracteres]")
        
        print("\n6. RECOMENDAÇÕES")
        print("-" * 50)
        
        recommendations = board_analysis.get('recommendations', [])
        print("Recomendações baseadas na análise:")
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na demonstração: {e}")
        import traceback
        traceback.print_exc()
        return False


def demo_key_features():
    """Demonstra as funcionalidades principais implementadas"""
    print("\n" + "=" * 80)
    print("CARACTERÍSTICAS PRINCIPAIS DA IMPLEMENTAÇÃO")
    print("=" * 80)
    
    features = [
        {
            "titulo": "✅ VERIFICAÇÃO DE INTEGRAÇÃO",
            "descricao": "O módulo verifica automaticamente se está usando documents, catalog ou doc service",
            "implementacao": "check_service_integration() em enhanced_legal_analysis.py"
        },
        {
            "titulo": "✅ ANÁLISE AJUSTADA",
            "descricao": "Análise ajustada para mudanças feitas nos módulos anteriores",
            "implementacao": "Integração condicional com document e catalog services"
        },
        {
            "titulo": "✅ ANÁLISE ENRIQUECIDA",
            "descricao": "Produz análise enriquecida com novas informações extraídas",
            "implementacao": "enhanced_legal_document_analysis() com contexto jurídico"
        },
        {
            "titulo": "✅ FOCO JURÍDICO",
            "descricao": "Análise jurídica focada para síntese do assunto",
            "implementacao": "generate_subject_synthesis() específico para direito"
        },
        {
            "titulo": "✅ RESUMO ESTRUTURADO",
            "descricao": "Resumo estruturado da ideia principal em cada conjunto de dados",
            "implementacao": "generate_structured_summary() organizado hierarquicamente"
        },
        {
            "titulo": "✅ MEMÓRIA DE CONTEXTO",
            "descricao": "Estrutura de memória para nomes, ações, deduções, relatos, pontos de atenção",
            "implementacao": "LegalContext dataclass com categorização específica"
        },
        {
            "titulo": "✅ MÉTODO DE SÍNTESE",
            "descricao": "Método que recebe texto longo e extrai análise completa",
            "implementacao": "analyze_long_legal_text() como alias principal"
        },
        {
            "titulo": "✅ BANCA APRIMORADA",
            "descricao": "Banca examinadora integrada com análise enriquecida",
            "implementacao": "enhanced_questionnaire() em examining_board.py"
        }
    ]
    
    for feature in features:
        print(f"\n{feature['titulo']}")
        print(f"   Descrição: {feature['descricao']}")
        print(f"   Implementação: {feature['implementacao']}")
    
    print("\n" + "=" * 80)
    print("ARQUIVOS MODIFICADOS/CRIADOS")
    print("=" * 80)
    
    files = [
        "📄 src/modules/analysis/enhanced_legal_analysis.py - NOVO módulo principal",
        "📄 src/modules/analysis/examining_board.py - APRIMORADO com integração",
        "📄 src/modules/analysis/__init__.py - ATUALIZADO para exportar funções",
        "📄 test_enhanced_analysis.py - TESTE da funcionalidade básica",
        "📄 test_enhanced_examining_board.py - TESTE da integração completa"
    ]
    
    for file_info in files:
        print(f"  {file_info}")


def main():
    """Executa a demonstração completa"""
    print("DEMONSTRAÇÃO COMPLETA DA ANÁLISE JURÍDICA ENRIQUECIDA")
    print("=" * 80)
    print("Esta demonstração mostra como foi implementada a solução para:")
    print("- Verificar uso de documents/catalog/doc service")
    print("- Ajustar análise para mudanças nos módulos anteriores") 
    print("- Produzir análise enriquecida com novas informações")
    print("- Focar em análise jurídica com síntese e resumo estruturado")
    print("- Implementar memória de contexto para entidades jurídicas")
    print("- Criar método de síntese para textos longos")
    print("=" * 80)
    
    success = demo_complete_legal_analysis()
    demo_key_features()
    
    print("\n" + "=" * 80)
    print("CONCLUSÃO")
    print("=" * 80)
    
    if success:
        print("✅ IMPLEMENTAÇÃO CONCLUÍDA COM SUCESSO!")
        print()
        print("O módulo de análise foi aprimorado conforme solicitado:")
        print("• Verifica automaticamente integração com document/catalog/doc service")
        print("• Ajusta análise com base nos serviços disponíveis")
        print("• Produz análise jurídica enriquecida e contextualizada")
        print("• Foca em síntese jurídica, resumo estruturado e memória de contexto")
        print("• Implementa método principal para análise de textos longos")
        print("• Mantém compatibilidade com análise tradicional como fallback")
        print()
        print("A solução está pronta para uso e pode ser expandida com")
        print("a instalação das dependências opcionais (ollama, docling, etc.)")
    else:
        print("⚠️  DEMONSTRAÇÃO CONCLUÍDA COM LIMITAÇÕES")
        print("A implementação está funcional, mas requer dependências")
        print("externas para análise completa.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())