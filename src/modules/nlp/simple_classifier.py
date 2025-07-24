# flake8: noqa: E501

import re
import os
import logging
import traceback
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from collections import Counter

# Importações condicionais do módulo de análise
try:
    from src.modules.analysis.legislation import (
        categories, normative_types, nomatives,
        set_a_title, define_categories, define_the_normative_type,
        extract_entities, extract_the_penalties, define_the_legal_terms,
        extract_legal_dates_and_deadlines, summarize
    )
    ANALYSIS_AVAILABLE = True
except ImportError:
    ANALYSIS_AVAILABLE = False
    categories = []
    normative_types = []
    nomatives = []

# Importações condicionais do módulo de documento
try:
    from src.modules.document.service import document_content, document_paragraphs_with_details
    DOCUMENT_AVAILABLE = True
except ImportError:
    DOCUMENT_AVAILABLE = False


class ClassificationType(Enum):
    """Tipos de classificação suportados"""
    SUBJECT = "subject"
    TITLE = "title"
    ARTICLE_TYPE = "article_type"
    LEGAL_CATEGORY = "legal_category"
    NORMATIVE_TYPE = "normative_type"
    LEGAL_INTENTION = "legal_intention"


class SimpleLegalClassifier:
    """
    Classificador simplificado para documentos legais usando regras e padrões
    Não depende de bibliotecas externas como sklearn
    """
    
    def __init__(self):
        # Categorias padrão para classificação de assunto
        self.subject_patterns = {
            "Direitos Fundamentais": [
                "livre", "manifestação", "pensamento", "iguais", "perante", "lei", "direitos",
                "liberdade", "expressão", "consciência", "crença", "religião"
            ],
            "Processo Judicial": [
                "processo", "petição", "inicial", "recurso", "prazo", "audiência", "sentença",
                "apelação", "execução", "citação", "intimação"
            ],
            "Administração Pública": [
                "administração", "pública", "princípios", "legalidade", "impessoalidade",
                "moralidade", "publicidade", "eficiência", "servidor"
            ],
            "Contratos e Obrigações": [
                "contrato", "obrigação", "devedor", "credor", "pagamento", "prestação",
                "acordo", "convenção", "ajuste"
            ],
            "Família e Sucessões": [
                "casamento", "união", "estável", "família", "herança", "sucessão",
                "testamento", "inventário", "cônjuge"
            ],
            "Propriedade e Posse": [
                "propriedade", "posse", "domínio", "bem", "imóvel", "móvel",
                "aquisição", "alienação", "registro"
            ],
            "Responsabilidade Civil": [
                "dano", "indenização", "responsabilidade", "culpa", "negligência",
                "reparação", "prejuízo", "lesão"
            ],
            "Tributação": [
                "imposto", "taxa", "contribuição", "tributo", "arrecadação",
                "fisco", "receita", "alíquota", "base de cálculo"
            ],
            "Trabalho e Emprego": [
                "trabalho", "emprego", "trabalhador", "empregador", "salário",
                "jornada", "férias", "rescisão", "contrato de trabalho"
            ],
            "Meio Ambiente": [
                "meio ambiente", "natureza", "poluição", "preservação",
                "sustentabilidade", "ecologia", "recursos naturais"
            ],
            "Consumidor": [
                "consumidor", "fornecedor", "produto", "serviço", "defeito",
                "vício", "garantia", "proteção"
            ],
            "Empresarial": [
                "empresa", "sociedade", "comercial", "atividade econômica",
                "registro", "junta comercial", "cnpj"
            ],
            "Penal": [
                "crime", "delito", "pena", "prisão", "reclusão", "detenção",
                "contravenção", "infração"
            ],
            "Constitucional": [
                "constituição", "federal", "emenda", "constitucional",
                "poder", "república", "federação"
            ]
        }
        
        # Padrões para tipos de artigo
        self.article_patterns = {
            "Definição": [
                "considera-se", "define-se", "entende-se", "para os efeitos",
                "conceito", "definição", "significa"
            ],
            "Proibição": [
                "é vedado", "proibido", "não é permitido", "fica proibida",
                "é defeso", "não pode", "é ilegal"
            ],
            "Obrigação": [
                "deverá", "deve", "é obrigatório", "fica obrigado",
                "tem o dever", "responsável", "incumbe"
            ],
            "Direito": [
                "é assegurado", "tem direito", "direito de", "garantia",
                "faculdade", "prerrogativa", "pode"
            ],
            "Penalidade": [
                "multa", "pena", "sanção", "punição", "infração",
                "penalidade", "será punido", "incorrerá"
            ],
            "Procedimento": [
                "processo", "procedimento", "rito", "tramitação",
                "seguirá", "observará", "cumprirá"
            ],
            "Competência": [
                "compete", "competência", "atribuição", "cabe",
                "responsabilidade", "função"
            ],
            "Prazo": [
                "prazo", "dias", "meses", "anos", "dentro de",
                "no prazo", "até", "limite"
            ],
            "Revogação": [
                "revoga", "revogada", "ab-rogada", "derrogada",
                "sem efeito", "anulada"
            ],
            "Disposição Geral": [
                "disposições", "gerais", "finais", "transitórias",
                "regulamento", "normas"
            ]
        }
        
        # Padrões para intenções legais
        self.intention_patterns = {
            "Regulamentar": [
                "regulamenta", "disciplina", "estabelece normas",
                "fixa regras", "organiza"
            ],
            "Proibir": [
                "proíbe", "veda", "não permite", "é defeso",
                "fica proibido"
            ],
            "Autorizar": [
                "autoriza", "permite", "faculta", "concede",
                "fica autorizado"
            ],
            "Definir": [
                "define", "conceitua", "estabelece conceito",
                "determina", "fixa definição"
            ],
            "Estabelecer Prazo": [
                "prazo", "dentro de", "no prazo de", "até",
                "limite de tempo"
            ],
            "Criar Obrigação": [
                "obrigatório", "deverá", "deve", "fica obrigado",
                "tem o dever"
            ],
            "Conceder Direito": [
                "direito", "assegura", "garante", "concede",
                "reconhece"
            ],
            "Estabelecer Penalidade": [
                "punição", "multa", "pena", "sanção",
                "será punido"
            ],
            "Revogar": [
                "revoga", "anula", "cancela", "torna sem efeito",
                "ab-roga"
            ],
            "Alterar": [
                "altera", "modifica", "muda", "substitui",
                "passa a vigorar"
            ]
        }

    def _extract_keywords(self, text: str) -> List[str]:
        """Extrai palavras-chave do texto"""
        # Converter para minúsculas e extrair palavras
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        
        # Filtrar palavras muito curtas ou muito comuns
        stopwords = {'de', 'da', 'do', 'das', 'dos', 'a', 'o', 'as', 'os', 
                    'e', 'ou', 'em', 'para', 'por', 'com', 'que', 'se', 'na', 'no'}
        
        keywords = [word for word in words if len(word) > 2 and word not in stopwords]
        return keywords

    def _calculate_pattern_score(self, text: str, patterns: List[str]) -> float:
        """Calcula pontuação baseada na presença de padrões no texto"""
        text_lower = text.lower()
        score = 0.0
        total_patterns = len(patterns)
        
        if total_patterns == 0:
            return 0.0
        
        for pattern in patterns:
            if pattern.lower() in text_lower:
                score += 1.0
        
        return score / total_patterns

    def classify_subject(self, text: str) -> Optional[str]:
        """Classifica o assunto principal do texto"""
        best_category = None
        best_score = 0.0
        
        for category, patterns in self.subject_patterns.items():
            score = self._calculate_pattern_score(text, patterns)
            if score > best_score:
                best_score = score
                best_category = category
        
        # Só retorna se teve pelo menos alguma correspondência
        return best_category if best_score > 0.0 else "Direito Geral"

    def classify_article_type(self, text: str) -> Optional[str]:
        """Classifica o tipo de artigo"""
        best_type = None
        best_score = 0.0
        
        for article_type, patterns in self.article_patterns.items():
            score = self._calculate_pattern_score(text, patterns)
            if score > best_score:
                best_score = score
                best_type = article_type
        
        return best_type if best_score > 0.0 else "Disposição Geral"

    def classify_legal_intention(self, text: str) -> Optional[str]:
        """Classifica a intenção legal do texto"""
        best_intention = None
        best_score = 0.0
        
        for intention, patterns in self.intention_patterns.items():
            score = self._calculate_pattern_score(text, patterns)
            if score > best_score:
                best_score = score
                best_intention = intention
        
        return best_intention if best_score > 0.0 else "Regulamentar"

    def generate_title(self, text: str) -> str:
        """
        Gera um título apropriado para o texto
        Usa análise LLM se disponível, senão usa classificação baseada em palavras-chave
        """
        if ANALYSIS_AVAILABLE:
            try:
                return set_a_title(text)
            except Exception:
                pass
        
        # Fallback: gerar título baseado em palavras-chave
        keywords = self._extract_keywords(text)
        key_words = [w for w in keywords if len(w) > 3]
        
        if key_words:
            # Pegar as primeiras 5 palavras mais significativas
            title_words = key_words[:5]
            return ' '.join(title_words).title()
        
        return "Documento Legal"

    def classify_legal_category(self, text: str) -> str:
        """
        Classifica a categoria legal do texto
        """
        if ANALYSIS_AVAILABLE:
            try:
                return define_categories(text)
            except Exception:
                pass
        
        # Fallback: usar classificação por padrões
        return self.classify_subject(text) or "Direito Geral"

    def classify_normative_type(self, text: str) -> str:
        """
        Classifica o tipo normativo do texto
        """
        if ANALYSIS_AVAILABLE:
            try:
                return define_the_normative_type(text)
            except Exception:
                pass
        
        # Fallback: análise baseada em padrões
        text_lower = text.lower()
        if 'lei' in text_lower and 'complementar' in text_lower:
            return "Lei Complementar"
        elif 'emenda' in text_lower and 'constitucional' in text_lower:
            return "Emenda Constitucional"
        elif 'medida' in text_lower and 'provisória' in text_lower:
            return "Medida Provisória"
        elif 'decreto' in text_lower:
            return "Decreto"
        elif 'portaria' in text_lower:
            return "Portaria"
        elif 'resolução' in text_lower:
            return "Resolução"
        elif 'instrução' in text_lower and 'normativa' in text_lower:
            return "Instrução Normativa"
        elif 'lei' in text_lower:
            return "Lei"
        else:
            return "Lei"

    def analyze_document_content(self, document_path: str) -> Dict[str, Any]:
        """
        Analisa o conteúdo completo de um documento e retorna classificações múltiplas
        """
        try:
            if not DOCUMENT_AVAILABLE:
                logging.warning("Módulo de documento não disponível")
                return {}
            
            # Extrair conteúdo do documento
            content = document_content(document_path)
            if not content:
                return {}
            
            # Analisar parágrafos para melhor granularidade
            paragraphs = document_paragraphs_with_details(document_path)
            
            results = {
                'document_path': document_path,
                'content_length': len(content),
                'paragraph_count': len(paragraphs),
                'classifications': {}
            }
            
            # Classificar documento completo
            results['classifications']['subject'] = self.classify_subject(content)
            results['classifications']['title'] = self.generate_title(content)
            results['classifications']['legal_category'] = self.classify_legal_category(content)
            results['classifications']['normative_type'] = self.classify_normative_type(content)
            
            # Analisar artigos individuais se disponível
            if paragraphs:
                article_analyses = []
                for i, paragraph in enumerate(paragraphs[:10]):  # Limitar a 10 parágrafos
                    if hasattr(paragraph, 'content') and paragraph.content:
                        para_content = paragraph.content
                        article_analysis = {
                            'paragraph_index': i,
                            'article_type': self.classify_article_type(para_content),
                            'legal_intention': self.classify_legal_intention(para_content),
                            'content_preview': para_content[:100] + "..." if len(para_content) > 100 else para_content
                        }
                        article_analyses.append(article_analysis)
                
                results['article_analyses'] = article_analyses
            
            return results
            
        except Exception as e:
            logging.error(f"Erro na análise do documento {document_path}: {e}\n{traceback.format_exc()}")
            return {}


# Instância global do classificador simples
_simple_classifier_instance = None

def get_simple_classifier() -> SimpleLegalClassifier:
    """Retorna instância singleton do classificador simples"""
    global _simple_classifier_instance
    if _simple_classifier_instance is None:
        _simple_classifier_instance = SimpleLegalClassifier()
    return _simple_classifier_instance