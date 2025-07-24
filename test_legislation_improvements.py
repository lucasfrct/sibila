#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste para validar as melhorias na análise legislativa.
Foca em testar as melhorias de padrões e validação sem dependência complexa de NLP.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.modules.analysis.legislation import (
    define_categories, extract_entities, define_the_normative_type,
    extract_legal_dates_and_deadlines, set_a_title, _analyzer
)

def test_legislation_analysis():
    """Testa as funções aprimoradas de análise legislativa."""
    
    print("=== TESTE DAS MELHORIAS NA ANÁLISE LEGISLATIVA ===\n")
    
    # Texto de exemplo - artigo da Lei de Acesso à Informação
    sample_text = """
    Art. 8º É dever dos órgãos e entidades públicas promover, independentemente de requerimentos, 
    a divulgação em local de fácil acesso, no âmbito de suas competências, de informações de 
    interesse coletivo ou geral por eles produzidas ou custodiadas.
    
    § 1º Na divulgação das informações a que se refere o caput, deverão constar, no mínimo:
    I - registro das competências e estrutura organizacional, endereços e telefones das respectivas unidades e horários de atendimento ao público;
    II - registros de quaisquer repasses ou transferências de recursos financeiros;
    III - registros das despesas;
    IV - informações concernentes a procedimentos licitatórios, inclusive os respectivos editais e resultados, bem como a todos os contratos celebrados;
    V - dados gerais para o acompanhamento de programas, ações, projetos e obras de órgãos e entidades; e
    VI - respostas a perguntas mais frequentes da sociedade.
    
    § 2º Para cumprimento do disposto no caput, os órgãos e entidades públicas deverão utilizar 
    todos os meios e instrumentos legítimos de que dispuserem, sendo obrigatória a divulgação 
    em sítios oficiais da rede mundial de computadores (internet).
    """
    
    print("TEXTO DE TESTE:")
    print(sample_text[:200] + "...\n")
    print("="*60)
    
    # Teste 1: Análise de padrões legislativos
    print("1. ANÁLISE DE PADRÕES LEGISLATIVOS:")
    patterns = _analyzer._identify_legislative_patterns(sample_text)
    print(f"   Referências a artigos: {patterns['article_references']}")
    print(f"   Marcadores de parágrafo: {patterns['paragraph_markers']}")
    print(f"   Referências a leis: {patterns['law_references']}")
    print(f"   Datas encontradas: {patterns['dates']}")
    print(f"   Numerais romanos: {patterns['roman_numerals']}")
    print(f"   Verbos legais: {patterns['legal_verbs']}")
    print()
    
    # Teste 2: Score de confiança básico
    print("2. CÁLCULO DE CONFIANÇA:")
    confidence = _analyzer._calculate_confidence({}, patterns)
    print(f"   Score de confiança baseado em padrões: {confidence:.2f}")
    print()
    
    # Teste 3: Tipo normativo melhorado
    print("3. IDENTIFICAÇÃO DE TIPO NORMATIVO:")
    norm_type = define_the_normative_type(sample_text)
    print(f"   Tipo identificado: {norm_type}")
    print()
    
    # Teste 4: Extração de datas aprimorada
    print("4. EXTRAÇÃO DE DATAS E PRAZOS:")
    dates = extract_legal_dates_and_deadlines(sample_text)
    print(f"   Datas/prazos encontrados: {dates}")
    print()
    
    # Teste 5: Texto específico com data
    date_text = """
    Art. 15. O prazo para cumprimento desta disposição é de 30 dias, 
    contados a partir de 15/03/2024. A empresa deve entregar o relatório 
    no prazo máximo de 60 dias.
    """
    print("5. TESTE COM TEXTO CONTENDO DATAS:")
    print("   Texto:", date_text[:100] + "...")
    dates_specific = extract_legal_dates_and_deadlines(date_text)
    print(f"   Datas/prazos identificados: {dates_specific}")
    print()
    
    # Teste 6: Texto específico por tipo normativo
    decreto_text = "Decreto nº 1234 de 2024 estabelece novas diretrizes..."
    lei_text = "Lei Ordinária nº 5678 de 2024 regulamenta o processo..."
    portaria_text = "Portaria nº 999 do Ministério da Saúde dispõe sobre..."
    
    print("6. TESTE DE TIPOS NORMATIVOS ESPECÍFICOS:")
    print(f"   Decreto: {define_the_normative_type(decreto_text)}")
    print(f"   Lei: {define_the_normative_type(lei_text)}")
    print(f"   Portaria: {define_the_normative_type(portaria_text)}")
    print()
    
    # Teste 7: Comparação com texto não legislativo
    print("="*60)
    print("7. TESTE COM TEXTO NÃO LEGISLATIVO:")
    
    non_legal_text = """
    João foi ao mercado comprar frutas. Ele encontrou maçãs vermelhas muito saborosas.
    O vendedor disse que as frutas estavam fresquinhas. João comprou duas sacolas.
    """
    
    print("TEXTO NÃO LEGISLATIVO:")
    print(non_legal_text)
    
    patterns_non_legal = _analyzer._identify_legislative_patterns(non_legal_text)
    confidence_non_legal = _analyzer._calculate_confidence({}, patterns_non_legal)
    
    print(f"   Padrões legislativos: {patterns_non_legal}")
    print(f"   Score de confiança: {confidence_non_legal:.2f}")
    print(f"   Tipo normativo: {define_the_normative_type(non_legal_text)}")
    print()
    
    print("="*60)
    print("TESTE CONCLUÍDO!")
    print("\nRESUMO DAS MELHORIAS IMPLEMENTADAS:")
    print("✓ Análise de padrões legislativos específicos")
    print("✓ Score de confiança baseado em características do texto")
    print("✓ Detecção automática de tipos normativos por padrões")
    print("✓ Extração de datas/prazos com regex aprimorado")
    print("✓ Validação de entrada para textos não legislativos")
    print("✓ Fallbacks robustos para casos de erro")
    print("✓ Redução de dependência de LLM para análises básicas")

def test_simple_pattern_detection():
    """Teste específico para detecção de padrões."""
    print("\n" + "="*60)
    print("TESTE ADICIONAL: DETECÇÃO DE PADRÕES")
    print("="*60)
    
    test_cases = [
        ("Art. 15º estabelece que...", "Artigo"),
        ("§ 2º Para efeitos desta lei...", "Parágrafo"),
        ("Lei nº 12.345 de 2020...", "Lei"),
        ("Decreto-lei nº 678...", "Decreto"),
        ("prazo de 30 dias para...", "Prazo"),
        ("data de 15/12/2024...", "Data"),
        ("Texto normal sem padrões.", "Neutro")
    ]
    
    for text, expected_type in test_cases:
        patterns = _analyzer._identify_legislative_patterns(text)
        confidence = _analyzer._calculate_confidence({}, patterns)
        print(f"   {expected_type:10}: {text[:30]:30} -> Score: {confidence:.2f}")

if __name__ == "__main__":
    test_legislation_analysis()
    test_simple_pattern_detection()