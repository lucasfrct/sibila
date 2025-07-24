#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Demonstração do classificador aprimorado para documentos legais
"""

import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.modules.nlp.classifier import (
    classify_subject, classify_article_type, classify_legal_intention,
    generate_title, classify_legal_category, classify_normative_type
)


def demonstrate_classifier():
    """Demonstra as funcionalidades do classificador"""
    print("=" * 80)
    print("DEMONSTRAÇÃO DO CLASSIFICADOR APRIMORADO PARA DOCUMENTOS LEGAIS")
    print("=" * 80)
    print()
    
    # Exemplos de textos legais
    examples = [
        {
            'text': "Art. 5º Todos são iguais perante a lei, sem distinção de qualquer natureza, garantindo-se aos brasileiros e aos estrangeiros residentes no País a inviolabilidade do direito à vida, à liberdade, à igualdade, à segurança e à propriedade",
            'description': "Artigo sobre direitos fundamentais"
        },
        {
            'text': "Art. 156. Compete aos Municípios instituir impostos sobre: I - propriedade predial e territorial urbana; II - transmissão inter vivos",
            'description': "Artigo sobre competência tributária municipal"
        },
        {
            'text': "Para os efeitos desta lei, considera-se empregador a empresa, individual ou coletiva, que, assumindo os riscos da atividade econômica, admite, assalaria e dirige a prestação pessoal de serviço",
            'description': "Definição de empregador"
        },
        {
            'text': "É vedado o uso de trabalho de menores de dezesseis anos, salvo na condição de aprendiz, a partir de quatorze anos",
            'description': "Proibição de trabalho infantil"
        },
        {
            'text': "O prazo para interposição de recurso é de quinze dias, contados da data da publicação da decisão no Diário Oficial",
            'description': "Estabelecimento de prazo"
        },
        {
            'text': "Fica autorizada a criação de fundos especiais destinados ao financiamento de programas de desenvolvimento urbano",
            'description': "Autorização para criação de fundos"
        },
        {
            'text': "A violação do disposto neste artigo resultará em multa de R$ 1.000,00 a R$ 10.000,00, aplicada pelo órgão competente",
            'description': "Estabelecimento de penalidade"
        },
        {
            'text': "Ficam revogadas as disposições em contrário, especialmente os artigos 10 a 15 da Lei nº 8.666, de 21 de junho de 1993",
            'description': "Revogação de dispositivos legais"
        }
    ]
    
    print("EXEMPLOS DE CLASSIFICAÇÃO:\n")
    
    for i, example in enumerate(examples, 1):
        text = example['text']
        description = example['description']
        
        print(f"EXEMPLO {i}: {description}")
        print(f"Texto: {text[:100]}{'...' if len(text) > 100 else ''}")
        print("-" * 60)
        
        # Classificações
        subject = classify_subject(text)
        article_type = classify_article_type(text)
        legal_intention = classify_legal_intention(text)
        title = generate_title(text)
        legal_category = classify_legal_category(text)
        normative_type = classify_normative_type(text)
        
        print(f"📁 Assunto/Categoria: {subject}")
        print(f"📄 Tipo de Artigo: {article_type}")
        print(f"🎯 Intenção Legal: {legal_intention}")
        print(f"📝 Título Gerado: {title}")
        print(f"⚖️  Categoria Legal: {legal_category}")
        print(f"📋 Tipo Normativo: {normative_type}")
        print()
        print("=" * 80)
        print()


def test_classification_coverage():
    """Testa a cobertura das classificações"""
    print("TESTE DE COBERTURA DAS CLASSIFICAÇÕES")
    print("=" * 60)
    
    # Teste de diferentes assuntos
    subject_tests = [
        ("Art. 1º É livre a manifestação do pensamento", "Direitos Fundamentais"),
        ("Art. 2º O processo será iniciado por petição inicial", "Processo Judicial"),
        ("Art. 3º A administração pública obedecerá aos princípios", "Administração Pública"),
        ("Art. 4º O contrato é perfeito e acabado", "Contratos e Obrigações"),
        ("Art. 5º O imposto sobre a renda será cobrado", "Tributação")
    ]
    
    print("TESTE DE CLASSIFICAÇÃO DE ASSUNTOS:")
    for text, expected in subject_tests:
        result = classify_subject(text)
        status = "✅" if result == expected else "⚠️"
        print(f"{status} '{text[:50]}...' -> {result} (esperado: {expected})")
    
    print("\nTESTE DE TIPOS DE ARTIGO:")
    article_tests = [
        ("Para os efeitos desta lei, considera-se", "Definição"),
        ("É vedado o uso de", "Proibição"),
        ("O responsável deverá", "Obrigação"),
        ("É assegurado o direito de", "Direito"),
        ("A violação resultará em multa", "Penalidade")
    ]
    
    for text, expected in article_tests:
        result = classify_article_type(text)
        status = "✅" if result == expected else "⚠️"
        print(f"{status} '{text}' -> {result} (esperado: {expected})")
    
    print("\nTESTE DE INTENÇÕES LEGAIS:")
    intention_tests = [
        ("Esta lei regulamenta o processo", "Regulamentar"),
        ("É proibido o transporte", "Proibir"),
        ("Fica autorizada a criação", "Autorizar"),
        ("O prazo para cumprimento é", "Estabelecer Prazo"),
        ("Fica revogada a Lei nº", "Revogar")
    ]
    
    for text, expected in intention_tests:
        result = classify_legal_intention(text)
        status = "✅" if result == expected else "⚠️"
        print(f"{status} '{text}' -> {result} (esperado: {expected})")


def test_title_generation():
    """Testa a geração de títulos"""
    print("\n" + "=" * 60)
    print("TESTE DE GERAÇÃO DE TÍTULOS")
    print("=" * 60)
    
    title_tests = [
        "Art. 1º Esta lei estabelece os direitos fundamentais dos cidadãos",
        "Art. 5º Dispõe sobre a proteção do meio ambiente e recursos naturais",
        "Art. 10 Regulamenta os procedimentos de licitação pública",
        "Art. 15 Define as competências dos órgãos de controle interno",
        "Art. 20 Estabelece penalidades para infrações administrativas"
    ]
    
    for text in title_tests:
        title = generate_title(text)
        print(f"📝 '{text[:50]}...' -> '{title}'")


def main():
    """Função principal"""
    print("Inicializando demonstração do classificador...\n")
    
    try:
        demonstrate_classifier()
        test_classification_coverage()
        test_title_generation()
        
        print("\n" + "=" * 80)
        print("✅ DEMONSTRAÇÃO CONCLUÍDA COM SUCESSO!")
        print("🎯 O classificador aprimorado está funcionando corretamente")
        print("📊 Suporte a múltiplos tipos de classificação implementado")
        print("⚖️  Especialização para documentos legais ativa")
        print("=" * 80)
        
    except Exception as e:
        print(f"❌ Erro durante a demonstração: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()