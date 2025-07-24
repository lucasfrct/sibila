# flake8: noqa: E501

import re
import os
import logging
import traceback
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from sklearn.multiclass import OneVsRestClassifier
from sklearn.pipeline import Pipeline

from joblib import dump, load

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


class LegalDocumentClassifier:
    """
    Classificador aprimorado para documentos legais que pode classificar:
    - Assunto/tópico principal
    - Título apropriado
    - Tipo de artigo
    - Categoria legal
    - Tipo normativo
    - Intenção legal
    """
    
    def __init__(self, model_path: str = "./models/legal_classifier"):
        self.model_path = model_path
        self.models: Dict[str, Pipeline] = {}
        self.vectorizers: Dict[str, TfidfVectorizer] = {}
        self.legal_categories = categories if ANALYSIS_AVAILABLE else []
        self.normative_types = normative_types if ANALYSIS_AVAILABLE else []
        
        # Garantir que o diretório de modelos existe
        os.makedirs(model_path, exist_ok=True)
        
        # Categorias padrão para classificação de assunto
        self.subject_categories = [
            "Direitos Fundamentais",
            "Processo Judicial", 
            "Administração Pública",
            "Contratos e Obrigações",
            "Família e Sucessões",
            "Propriedade e Posse",
            "Responsabilidade Civil",
            "Tributação",
            "Trabalho e Emprego",
            "Meio Ambiente",
            "Consumidor",
            "Empresarial",
            "Penal",
            "Constitucional"
        ]
        
        # Tipos de artigo
        self.article_types = [
            "Definição",
            "Proibição", 
            "Obrigação",
            "Direito",
            "Penalidade",
            "Procedimento",
            "Competência",
            "Prazo",
            "Revogação",
            "Disposição Geral"
        ]
        
        # Intenções legais
        self.legal_intentions = [
            "Regulamentar",
            "Proibir",
            "Autorizar", 
            "Definir",
            "Estabelecer Prazo",
            "Criar Obrigação",
            "Conceder Direito",
            "Estabelecer Penalidade",
            "Revogar",
            "Alterar"
        ]

    def _prepare_training_data(self, classification_type: ClassificationType) -> Tuple[List[str], List[str]]:
        """
        Prepara dados de treinamento sintéticos baseados no tipo de classificação
        """
        texts = []
        labels = []
        
        if classification_type == ClassificationType.SUBJECT:
            # Dados sintéticos para classificação de assunto
            synthetic_data = [
                ("Art. 1º É livre a manifestação do pensamento", "Direitos Fundamentais"),
                ("Art. 2º O processo será iniciado por petição inicial", "Processo Judicial"),
                ("Art. 3º A administração pública obedecerá aos princípios", "Administração Pública"),
                ("Art. 4º O contrato é perfeito e acabado", "Contratos e Obrigações"),
                ("Art. 5º O casamento é civil e gratuita a celebração", "Família e Sucessões"),
                ("Art. 6º A propriedade será exercida em consonância", "Propriedade e Posse"),
                ("Art. 7º Aquele que, por ação ou omissão voluntária", "Responsabilidade Civil"),
                ("Art. 8º O imposto sobre a renda será cobrado", "Tributação"),
                ("Art. 9º É direito dos trabalhadores urbanos e rurais", "Trabalho e Emprego"),
                ("Art. 10 Todos têm direito ao meio ambiente", "Meio Ambiente"),
                ("Art. 11 O consumidor tem direito à informação", "Consumidor"),
                ("Art. 12 A empresa deve seguir as normas", "Empresarial"),
                ("Art. 13 É crime contra a vida", "Penal"),
                ("Art. 14 A Constituição Federal estabelece", "Constitucional")
            ]
            texts, labels = zip(*synthetic_data)
            
        elif classification_type == ClassificationType.ARTICLE_TYPE:
            synthetic_data = [
                ("Para os efeitos desta lei, considera-se", "Definição"),
                ("É vedado o uso de", "Proibição"),
                ("O responsável deverá", "Obrigação"),
                ("É assegurado o direito de", "Direito"),
                ("A violação do disposto resultará em multa", "Penalidade"),
                ("O processo de licenciamento seguirá", "Procedimento"),
                ("Compete ao órgão competente", "Competência"),
                ("O prazo para recurso é de 30 dias", "Prazo"),
                ("Ficam revogadas as disposições", "Revogação"),
                ("As demais disposições regulamentares", "Disposição Geral")
            ]
            texts, labels = zip(*synthetic_data)
            
        elif classification_type == ClassificationType.LEGAL_INTENTION:
            synthetic_data = [
                ("Esta lei regulamenta o processo de", "Regulamentar"),
                ("É proibido o transporte de", "Proibir"),
                ("Fica autorizada a criação de", "Autorizar"),
                ("Para os fins desta lei, define-se", "Definir"),
                ("O prazo para cumprimento é de", "Estabelecer Prazo"),
                ("Fica obrigatório o uso de", "Criar Obrigação"),
                ("É assegurado o direito à", "Conceder Direito"),
                ("A infração será punida com", "Estabelecer Penalidade"),
                ("Fica revogada a Lei nº", "Revogar"),
                ("O artigo 5º passa a vigorar", "Alterar")
            ]
            texts, labels = zip(*synthetic_data)
        
        return list(texts), list(labels)

    def train_classifier(self, classification_type: ClassificationType, 
                        texts: Optional[List[str]] = None, 
                        labels: Optional[List[str]] = None,
                        test_size: float = 0.2) -> float:
        """
        Treina um classificador para o tipo especificado
        """
        try:
            # Usar dados fornecidos ou gerar dados sintéticos
            if texts is None or labels is None:
                texts, labels = self._prepare_training_data(classification_type)
            
            if not texts or not labels:
                raise ValueError(f"Não há dados de treinamento para {classification_type.value}")
            
            # Criar pipeline com vetorização e classificação
            pipeline = Pipeline([
                ('tfidf', TfidfVectorizer(
                    max_features=1000,
                    ngram_range=(1, 3),
                    stop_words=None,  # Manter stopwords para português legal
                    lowercase=True
                )),
                ('classifier', LogisticRegression(
                    random_state=42,
                    max_iter=1000,
                    multi_class='ovr'
                ))
            ])
            
            # Dividir dados em treino e teste
            if len(texts) > 1:
                X_train, X_test, y_train, y_test = train_test_split(
                    texts, labels, test_size=test_size, random_state=42, stratify=labels
                )
            else:
                X_train, X_test, y_train, y_test = texts, texts, labels, labels
            
            # Treinar modelo
            pipeline.fit(X_train, y_train)
            
            # Avaliar modelo
            if len(X_test) > 0:
                predictions = pipeline.predict(X_test)
                accuracy = accuracy_score(y_test, predictions)
                logging.info(f"Acurácia do modelo {classification_type.value}: {accuracy:.2f}")
            else:
                accuracy = 1.0
            
            # Salvar modelo
            self.models[classification_type.value] = pipeline
            self._save_model(classification_type, pipeline)
            
            return accuracy
            
        except Exception as e:
            logging.error(f"Erro ao treinar classificador {classification_type.value}: {e}\n{traceback.format_exc()}")
            return 0.0

    def _save_model(self, classification_type: ClassificationType, pipeline: Pipeline):
        """Salva o modelo treinado"""
        model_file = os.path.join(self.model_path, f"{classification_type.value}.joblib")
        dump(pipeline, model_file)

    def _load_model(self, classification_type: ClassificationType) -> Optional[Pipeline]:
        """Carrega um modelo salvo"""
        try:
            model_file = os.path.join(self.model_path, f"{classification_type.value}.joblib")
            if os.path.exists(model_file):
                return load(model_file)
            return None
        except Exception as e:
            logging.error(f"Erro ao carregar modelo {classification_type.value}: {e}")
            return None

    def classify_text(self, text: str, classification_type: ClassificationType) -> Optional[str]:
        """
        Classifica um texto usando o tipo de classificação especificado
        """
        try:
            # Carregar modelo se não estiver em memória
            if classification_type.value not in self.models:
                pipeline = self._load_model(classification_type)
                if pipeline is None:
                    # Treinar modelo se não existir
                    self.train_classifier(classification_type)
                    pipeline = self.models.get(classification_type.value)
                
                if pipeline is not None:
                    self.models[classification_type.value] = pipeline
            
            pipeline = self.models.get(classification_type.value)
            if pipeline is None:
                logging.warning(f"Modelo {classification_type.value} não disponível")
                return None
            
            # Fazer predição
            prediction = pipeline.predict([text])
            return prediction[0] if prediction else None
            
        except Exception as e:
            logging.error(f"Erro na classificação {classification_type.value}: {e}")
            return None

    def classify_subject(self, text: str) -> Optional[str]:
        """Classifica o assunto principal do texto"""
        return self.classify_text(text, ClassificationType.SUBJECT)

    def classify_article_type(self, text: str) -> Optional[str]:
        """Classifica o tipo de artigo"""
        return self.classify_text(text, ClassificationType.ARTICLE_TYPE)

    def classify_legal_intention(self, text: str) -> Optional[str]:
        """Classifica a intenção legal do texto"""
        return self.classify_text(text, ClassificationType.LEGAL_INTENTION)

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
        words = re.findall(r'\b\w+\b', text.lower())
        key_words = [w for w in words if len(w) > 3 and w not in ['artigo', 'para', 'esta', 'será', 'deve']]
        if key_words:
            return ' '.join(key_words[:5]).title()
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
        
        # Fallback: usar classificador treinado
        result = self.classify_text(text, ClassificationType.LEGAL_CATEGORY)
        return result if result else "Direito Geral"

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
        if 'lei' in text_lower:
            return "Lei"
        elif 'decreto' in text_lower:
            return "Decreto"
        elif 'portaria' in text_lower:
            return "Portaria"
        elif 'resolução' in text_lower:
            return "Resolução"
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

    def train_all_classifiers(self):
        """
        Treina todos os classificadores com dados sintéticos
        """
        results = {}
        for classification_type in ClassificationType:
            try:
                accuracy = self.train_classifier(classification_type)
                results[classification_type.value] = accuracy
                logging.info(f"Classificador {classification_type.value} treinado com acurácia: {accuracy:.2f}")
            except Exception as e:
                logging.error(f"Erro ao treinar {classification_type.value}: {e}")
                results[classification_type.value] = 0.0
        
        return results


# Instância global do classificador
_classifier_instance = None

def get_classifier() -> LegalDocumentClassifier:
    """Retorna instância singleton do classificador"""
    global _classifier_instance
    if _classifier_instance is None:
        _classifier_instance = LegalDocumentClassifier()
    return _classifier_instance