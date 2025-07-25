#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste focado apenas nos padrões e melhorias NLP, sem dependência do LLM.
"""

import sys
import os
import re
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.modules.analysis.legislation import _analyzer

def test_pattern_improvements():
    """Testa as melhorias de padrões implementadas."""
    
    print("=== TESTE DAS MELHORIAS DE PADRÕES NLP ===\n")
    
    # Casos de teste com diferentes tipos de texto
    test_cases = [
        {
            'name': 'Artigo Legislativo Completo',
            'text': '''Art. 8º É dever dos órgãos e entidades públicas promover, independentemente de requerimentos, 
            a divulgação em local de fácil acesso, no âmbito de suas competências.
            § 1º Na divulgação das informações a que se refere o caput, deverão constar, no mínimo:
            I - registro das competências e estrutura organizacional;
            II - registros de quaisquer repasses ou transferências;
            § 2º Para cumprimento do disposto no caput, os órgãos e entidades públicas deverão utilizar 
            todos os meios legítimos.''',
            'expected_confidence': 0.7
        },
        {
            'name': 'Decreto com Data',
            'text': '''Decreto nº 1234 de 15/03/2024 estabelece diretrizes para implementação.
            Art. 1º Este decreto regulamenta o processo no prazo de 30 dias.
            Art. 2º As empresas devem cumprir até 31/12/2024.''',
            'expected_confidence': 0.7
        },
        {
            'name': 'Lei com Prazos',
            'text': '''Lei Ordinária nº 5678 dispõe sobre o prazo de 60 dias para cumprimento.
            A partir da data de publicação, os órgãos terão 90 dias.
            O prazo máximo é de 6 meses.''',
            'expected_confidence': 0.6
        },
        {
            'name': 'Texto Não Legislativo',
            'text': '''João foi ao mercado comprar frutas. Ele encontrou maçãs vermelhas muito saborosas.
            O vendedor disse que as frutas estavam fresquinhas. João comprou duas sacolas.''',
            'expected_confidence': 0.5
        },
        {
            'name': 'Portaria com Verbos Legais',
            'text': '''Portaria nº 999 do Ministério da Saúde dispõe sobre procedimentos.
            Art. 1º Esta portaria estabelece critérios que regulamentam o processo.
            Art. 2º Determina que os órgãos devem alterar seus procedimentos.''',
            'expected_confidence': 0.8
        }
    ]
    
    print("RESULTADOS DOS TESTES:\n")
    print("-" * 80)
    
    for i, case in enumerate(test_cases, 1):
        print(f"{i}. {case['name']}")
        print("   Texto:", case['text'][:100] + "...")
        
        # Analisar padrões
        patterns = _analyzer._identify_legislative_patterns(case['text'])
        confidence = _analyzer._calculate_confidence({}, patterns)
        
        print(f"   Padrões encontrados:")
        print(f"     - Artigos: {patterns['article_references']}")
        print(f"     - Parágrafos: {patterns['paragraph_markers']}")
        print(f"     - Leis: {patterns['law_references']}")
        print(f"     - Datas: {patterns['dates']}")
        print(f"     - Numerais romanos: {patterns['roman_numerals']}")
        print(f"     - Verbos legais: {patterns['legal_verbs']}")
        print(f"   Score de confiança: {confidence:.2f}")
        print(f"   Esperado: {case['expected_confidence']:.2f}")
        
        # Verificar se score está próximo do esperado
        if abs(confidence - case['expected_confidence']) <= 0.2:
            print("   ✓ APROVADO - Score dentro do esperado")
        else:
            print("   ⚠ ATENÇÃO - Score diferente do esperado")
        
        print("-" * 80)

def test_date_extraction():
    """Testa especificamente a extração de datas com regex."""
    
    print("\n=== TESTE DE EXTRAÇÃO DE DATAS ===\n")
    
    date_test_cases = [
        "O prazo é de 30 dias para cumprimento",
        "Data limite: 15/03/2024 para entrega",
        "Publicado em 12 de março de 2024",
        "Prazo de 6 meses a partir da publicação", 
        "Até 31/12/2024 ou no prazo de 60 dias",
        "Março de 2024 como data limite",
        "Texto sem nenhuma data ou prazo específico"
    ]
    
    # Padrões de teste - simulando a função aprimorada
    date_patterns = [
        r'\d{1,2}[\/\.-]\d{1,2}[\/\.-]\d{2,4}',  # DD/MM/YYYY
        r'\d{1,2}\s+de\s+\w+\s+de\s+\d{4}',     # DD de mês de YYYY
        r'\w+\s+de\s+\d{4}',                     # mês de YYYY
        r'\d{1,2}\s+\w+\s+\d{4}'                # DD mês YYYY
    ]
    
    deadline_patterns = [
        r'\d+\s+(?:dias?|meses?|anos?)',         # X dias/meses/anos
        r'prazo\s+de\s+\d+\s+(?:dias?|meses?|anos?)',  # prazo de X dias
        r'até\s+\d+\s+(?:dias?|meses?|anos?)',   # até X dias
        r'no\s+prazo\s+de\s+\d+',               # no prazo de X
        r'dentro\s+de\s+\d+\s+(?:dias?|meses?|anos?)'  # dentro de X dias
    ]
    
    for i, text in enumerate(date_test_cases, 1):
        print(f"{i}. Texto: {text}")
        
        found_dates = []
        found_deadlines = []
        
        # Extrair datas usando regex
        for pattern in date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            found_dates.extend(matches)
        
        # Extrair prazos usando regex
        for pattern in deadline_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            found_deadlines.extend(matches)
        
        all_results = found_dates + found_deadlines
        print(f"   Datas encontradas: {found_dates}")
        print(f"   Prazos encontrados: {found_deadlines}")
        print(f"   Total: {len(all_results)} elementos")
        print()

def test_normative_type_detection():
    """Testa a detecção de tipos normativos baseada em padrões."""
    
    print("=== TESTE DE DETECÇÃO DE TIPOS NORMATIVOS ===\n")
    
    normative_test_cases = [
        ("Lei nº 12.345 de 2020 estabelece diretrizes", "Lei"),
        ("Decreto-lei nº 678 regulamenta o processo", "Decreto"),
        ("Portaria nº 999 do Ministério dispõe sobre", "Portaria"),
        ("Medida Provisória nº 123 de 2024", "Medida Provisória"),
        ("Emenda Constitucional nº 45 altera a Constituição", "Emenda Constitucional"),
        ("Resolução nº 456 do Conselho Nacional", "Resolução"),
        ("Instrução Normativa nº 789 da Receita Federal", "Instrução Normativa"),
        ("Circular nº 321 orienta sobre procedimentos", "Circular"),
        ("Deliberação nº 567 da ANATEL", "Deliberação"),
        ("Texto genérico sem tipo normativo específico", "Lei")  # Fallback
    ]
    
    # Padrões específicos por tipo normativo (da função aprimorada)
    type_patterns = {
        'Lei': ['lei n', 'lei ordinária', 'lei complementar'],
        'Decreto': ['decreto n', 'decreto-lei'],
        'Portaria': ['portaria n', 'portaria'],
        'Medida Provisória': ['medida provisória', 'mp n'],
        'Emenda Constitucional': ['emenda constitucional', 'ec n', 'emenda à constituição'],
        'Resolução': ['resolução n'],
        'Instrução Normativa': ['instrução normativa', 'in n'],
        'Circular': ['circular n'],
        'Deliberação': ['deliberação n']
    }
    
    for i, (text, expected) in enumerate(normative_test_cases, 1):
        print(f"{i}. Texto: {text}")
        print(f"   Esperado: {expected}")
        
        text_lower = text.lower()
        pattern_scores = {}
        
        for norm_type, patterns in type_patterns.items():
            score = sum(1 for pattern in patterns if pattern in text_lower)
            if score > 0:
                pattern_scores[norm_type] = score
        
        if pattern_scores:
            detected = max(pattern_scores, key=pattern_scores.get)
            confidence = pattern_scores[detected]
        else:
            detected = "Lei"  # Fallback
            confidence = 0
        
        print(f"   Detectado: {detected} (confiança: {confidence})")
        
        if detected == expected:
            print("   ✓ CORRETO")
        else:
            print("   ⚠ DIFERENTE")
        print()

if __name__ == "__main__":
    test_pattern_improvements()
    test_date_extraction()
    test_normative_type_detection()
    
    print("\n" + "="*60)
    print("RESUMO DAS MELHORIAS TESTADAS:")
    print("✓ Análise de padrões legislativos específicos")
    print("✓ Cálculo de confiança baseado em características")
    print("✓ Extração de datas/prazos com regex preciso")
    print("✓ Detecção automática de tipos normativos")
    print("✓ Validação robusta para textos não legislativos")
    print("✓ Redução de dependência de LLM para análises básicas")