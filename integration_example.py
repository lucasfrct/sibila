#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Exemplo de integração do classificador aprimorado com os módulos de documento, catálogo e análise
Demonstra como usar o novo classificador para facilitar o processo de análise de documentos legais
"""

import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.modules.nlp.classifier import (
    classify_subject, classify_article_type, classify_legal_intention,
    generate_title, classify_legal_category, classify_normative_type,
    classify_document
)


def simulate_document_analysis():
    """
    Simula a análise de um documento legal completo usando o classificador aprimorado
    """
    print("=" * 80)
    print("INTEGRAÇÃO DO CLASSIFICADOR COM ANÁLISE DE DOCUMENTOS LEGAIS")
    print("=" * 80)
    print()
    
    # Simular conteúdo de um documento legal
    document_content = """
    LEI Nº 12.345, DE 1º DE JANEIRO DE 2023
    
    Dispõe sobre a proteção de dados pessoais e dá outras providências.
    
    Art. 1º Esta lei estabelece normas gerais sobre tratamento de dados pessoais, 
    pessoa física ou jurídica, de direito público ou privado, com o objetivo de 
    proteger os direitos fundamentais de liberdade e de privacidade.
    
    Art. 2º Para os efeitos desta lei, considera-se:
    I - dado pessoal: informação relacionada a pessoa natural identificada;
    II - tratamento: toda operação realizada com dados pessoais.
    
    Art. 3º É vedado o tratamento de dados pessoais sem o consentimento expresso 
    do titular, salvo nas hipóteses previstas nesta lei.
    
    Art. 4º É assegurado ao titular dos dados o direito de acesso, retificação, 
    portabilidade e eliminação de seus dados pessoais.
    
    Art. 5º A violação do disposto nesta lei resultará em multa de R$ 2.000,00 
    a R$ 50.000,00, aplicada pela autoridade competente.
    
    Art. 6º O prazo para adequação às disposições desta lei é de 180 dias, 
    contados da data de sua publicação.
    
    Art. 7º Esta lei entra em vigor na data de sua publicação.
    
    Art. 8º Ficam revogadas as disposições em contrário.
    """
    
    print("📄 DOCUMENTO: Lei sobre proteção de dados pessoais")
    print("=" * 60)
    print()
    
    # Análise do documento completo
    print("🔍 ANÁLISE GERAL DO DOCUMENTO:")
    doc_subject = classify_subject(document_content)
    doc_title = generate_title(document_content)
    doc_category = classify_legal_category(document_content)
    doc_normative_type = classify_normative_type(document_content)
    
    print(f"📁 Assunto Principal: {doc_subject}")
    print(f"📝 Título Sugerido: {doc_title}")
    print(f"⚖️  Categoria Legal: {doc_category}")
    print(f"📋 Tipo Normativo: {doc_normative_type}")
    print()
    
    # Análise de artigos individuais
    articles = [
        {
            'number': 1,
            'text': "Esta lei estabelece normas gerais sobre tratamento de dados pessoais, pessoa física ou jurídica, de direito público ou privado, com o objetivo de proteger os direitos fundamentais de liberdade e de privacidade."
        },
        {
            'number': 2,
            'text': "Para os efeitos desta lei, considera-se: I - dado pessoal: informação relacionada a pessoa natural identificada; II - tratamento: toda operação realizada com dados pessoais."
        },
        {
            'number': 3,
            'text': "É vedado o tratamento de dados pessoais sem o consentimento expresso do titular, salvo nas hipóteses previstas nesta lei."
        },
        {
            'number': 4,
            'text': "É assegurado ao titular dos dados o direito de acesso, retificação, portabilidade e eliminação de seus dados pessoais."
        },
        {
            'number': 5,
            'text': "A violação do disposto nesta lei resultará em multa de R$ 2.000,00 a R$ 50.000,00, aplicada pela autoridade competente."
        },
        {
            'number': 6,
            'text': "O prazo para adequação às disposições desta lei é de 180 dias, contados da data de sua publicação."
        }
    ]
    
    print("📋 ANÁLISE DETALHADA DOS ARTIGOS:")
    print("-" * 60)
    
    for article in articles:
        article_num = article['number']
        article_text = article['text']
        
        # Classificações do artigo
        art_type = classify_article_type(article_text)
        art_intention = classify_legal_intention(article_text)
        art_subject = classify_subject(article_text)
        
        print(f"\n📍 Art. {article_num}º")
        print(f"   📄 Tipo: {art_type}")
        print(f"   🎯 Intenção: {art_intention}")
        print(f"   📁 Assunto: {art_subject}")
        print(f"   📝 Resumo: {article_text[:80]}...")
    
    print()
    print("=" * 80)
    print("💡 RELATÓRIO DE ANÁLISE CONTEXTUAL")
    print("=" * 80)
    
    # Criar relatório contextual
    analysis_summary = generate_analysis_report(document_content, articles)
    print(analysis_summary)


def generate_analysis_report(document_content, articles):
    """
    Gera um relatório de análise contextual baseado nas classificações
    """
    # Contadores para análise estatística
    article_types = {}
    intentions = {}
    subjects = {}
    
    for article in articles:
        art_type = classify_article_type(article['text'])
        art_intention = classify_legal_intention(article['text'])
        art_subject = classify_subject(article['text'])
        
        article_types[art_type] = article_types.get(art_type, 0) + 1
        intentions[art_intention] = intentions.get(art_intention, 0) + 1
        subjects[art_subject] = subjects.get(art_subject, 0) + 1
    
    # Gerar relatório
    report = []
    report.append("🔢 ESTATÍSTICAS DE CLASSIFICAÇÃO:")
    report.append("")
    
    report.append("📄 Tipos de Artigo mais frequentes:")
    for art_type, count in sorted(article_types.items(), key=lambda x: x[1], reverse=True):
        report.append(f"   • {art_type}: {count} ocorrência(s)")
    report.append("")
    
    report.append("🎯 Intenções Legais identificadas:")
    for intention, count in sorted(intentions.items(), key=lambda x: x[1], reverse=True):
        report.append(f"   • {intention}: {count} ocorrência(s)")
    report.append("")
    
    report.append("📁 Assuntos abordados:")
    for subject, count in sorted(subjects.items(), key=lambda x: x[1], reverse=True):
        report.append(f"   • {subject}: {count} ocorrência(s)")
    report.append("")
    
    # Análise contextual
    report.append("🎯 ANÁLISE CONTEXTUAL:")
    report.append("")
    
    main_subject = classify_subject(document_content)
    main_normative = classify_normative_type(document_content)
    
    if "Definição" in article_types:
        report.append("✅ Documento possui artigos de definição, facilitando interpretação")
    
    if "Penalidade" in article_types:
        report.append("⚠️  Documento estabelece penalidades - requer atenção especial")
    
    if "Prazo" in article_types:
        report.append("⏰ Documento estabelece prazos - verificar cumprimento")
    
    if main_subject == "Direitos Fundamentais":
        report.append("🏛️  Documento trata de direitos fundamentais - alta relevância")
    
    if main_normative == "Lei":
        report.append("📜 Documento é uma lei - força normativa plena")
    
    report.append("")
    report.append("💡 RECOMENDAÇÕES PARA ANÁLISE:")
    report.append("")
    report.append("1. Focar nos artigos de definição para compreensão conceitual")
    report.append("2. Dar atenção especial aos artigos de penalidade")
    report.append("3. Verificar prazos estabelecidos e sua aplicabilidade")
    report.append("4. Considerar o contexto de proteção de dados na interpretação")
    
    return "\n".join(report)


def demonstrate_classification_benefits():
    """
    Demonstra os benefícios do classificador para o processo de análise
    """
    print("\n" + "=" * 80)
    print("🎯 BENEFÍCIOS DO CLASSIFICADOR PARA ANÁLISE LEGAL")
    print("=" * 80)
    print()
    
    benefits = [
        {
            'title': "🏷️  Categorização Automática",
            'description': "Identifica automaticamente o assunto e categoria legal do documento"
        },
        {
            'title': "📄 Tipificação de Artigos",
            'description': "Classifica cada artigo por tipo (definição, proibição, etc.)"
        },
        {
            'title': "🎯 Identificação de Intenções",
            'description': "Determina a intenção legislativa (regulamentar, proibir, etc.)"
        },
        {
            'title': "📝 Geração de Títulos",
            'description': "Cria títulos descritivos para facilitar indexação"
        },
        {
            'title': "⚖️  Contextualização Legal",
            'description': "Fornece contexto legal apropriado para análise"
        },
        {
            'title': "📊 Análise Estatística",
            'description': "Permite análise quantitativa dos tipos de dispositivos"
        },
        {
            'title': "🔍 Busca Aprimorada",
            'description': "Melhora a capacidade de busca e recuperação de informação"
        },
        {
            'title': "⚡ Processamento Eficiente",
            'description': "Acelera o processo de análise e compreensão de documentos"
        }
    ]
    
    for benefit in benefits:
        print(f"{benefit['title']}")
        print(f"   {benefit['description']}")
        print()


def main():
    """Função principal"""
    print("🚀 Demonstração de Integração do Classificador Aprimorado")
    print()
    
    try:
        simulate_document_analysis()
        demonstrate_classification_benefits()
        
        print("✅ DEMONSTRAÇÃO CONCLUÍDA COM SUCESSO!")
        print()
        print("🎯 O classificador aprimorado está pronto para uso em produção")
        print("📚 Suporte completo para análise de documentos legais implementado")
        print("⚖️  Facilitação do processo de análise legal alcançada")
        
    except Exception as e:
        print(f"❌ Erro durante a demonstração: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()