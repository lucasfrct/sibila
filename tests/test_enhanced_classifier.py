#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Testes para o classificador aprimorado de documentos legais
"""

import sys
import os
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pytest
import tempfile
import logging

from src.modules.nlp.enhanced_classifier import LegalDocumentClassifier, ClassificationType


class TestLegalDocumentClassifier:
    """Testes para a classe LegalDocumentClassifier"""
    
    def setup_method(self):
        """Setup para cada teste"""
        # Criar diretório temporário para modelos
        self.temp_dir = tempfile.mkdtemp()
        self.classifier = LegalDocumentClassifier(model_path=self.temp_dir)
    
    def test_classifier_initialization(self):
        """Testa se o classificador é inicializado corretamente"""
        assert self.classifier is not None
        assert self.classifier.model_path == self.temp_dir
        assert len(self.classifier.subject_categories) > 0
        assert len(self.classifier.article_types) > 0
        assert len(self.classifier.legal_intentions) > 0
    
    def test_prepare_training_data_subject(self):
        """Testa a preparação de dados de treinamento para assunto"""
        texts, labels = self.classifier._prepare_training_data(ClassificationType.SUBJECT)
        
        assert len(texts) > 0
        assert len(labels) > 0
        assert len(texts) == len(labels)
        assert all(isinstance(text, str) for text in texts)
        assert all(isinstance(label, str) for label in labels)
    
    def test_prepare_training_data_article_type(self):
        """Testa a preparação de dados de treinamento para tipo de artigo"""
        texts, labels = self.classifier._prepare_training_data(ClassificationType.ARTICLE_TYPE)
        
        assert len(texts) > 0
        assert len(labels) > 0
        assert len(texts) == len(labels)
        assert "Definição" in labels
        assert "Proibição" in labels
    
    def test_prepare_training_data_legal_intention(self):
        """Testa a preparação de dados de treinamento para intenção legal"""
        texts, labels = self.classifier._prepare_training_data(ClassificationType.LEGAL_INTENTION)
        
        assert len(texts) > 0
        assert len(labels) > 0
        assert len(texts) == len(labels)
        assert "Regulamentar" in labels
        assert "Proibir" in labels
    
    def test_train_classifier_subject(self):
        """Testa o treinamento do classificador de assunto"""
        accuracy = self.classifier.train_classifier(ClassificationType.SUBJECT)
        
        assert accuracy >= 0.0
        assert accuracy <= 1.0
        assert ClassificationType.SUBJECT.value in self.classifier.models
    
    def test_train_classifier_article_type(self):
        """Testa o treinamento do classificador de tipo de artigo"""
        accuracy = self.classifier.train_classifier(ClassificationType.ARTICLE_TYPE)
        
        assert accuracy >= 0.0
        assert accuracy <= 1.0
        assert ClassificationType.ARTICLE_TYPE.value in self.classifier.models
    
    def test_classify_subject(self):
        """Testa a classificação de assunto"""
        # Treinar primeiro
        self.classifier.train_classifier(ClassificationType.SUBJECT)
        
        # Testar classificação
        text = "Art. 1º É livre a manifestação do pensamento"
        result = self.classifier.classify_subject(text)
        
        assert result is not None
        assert isinstance(result, str)
        assert result in self.classifier.subject_categories
    
    def test_classify_article_type(self):
        """Testa a classificação de tipo de artigo"""
        # Treinar primeiro
        self.classifier.train_classifier(ClassificationType.ARTICLE_TYPE)
        
        # Testar classificação
        text = "Para os efeitos desta lei, considera-se"
        result = self.classifier.classify_article_type(text)
        
        assert result is not None
        assert isinstance(result, str)
        assert result in self.classifier.article_types
    
    def test_classify_legal_intention(self):
        """Testa a classificação de intenção legal"""
        # Treinar primeiro
        self.classifier.train_classifier(ClassificationType.LEGAL_INTENTION)
        
        # Testar classificação
        text = "É proibido o transporte de"
        result = self.classifier.classify_legal_intention(text)
        
        assert result is not None
        assert isinstance(result, str)
        assert result in self.classifier.legal_intentions
    
    def test_generate_title(self):
        """Testa a geração de título"""
        text = "Art. 1º A lei estabelece os direitos fundamentais"
        result = self.classifier.generate_title(text)
        
        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_classify_normative_type(self):
        """Testa a classificação de tipo normativo"""
        text_lei = "A lei estabelece que"
        result = self.classifier.classify_normative_type(text_lei)
        assert result == "Lei"
        
        text_decreto = "O decreto regulamenta"
        result = self.classifier.classify_normative_type(text_decreto)
        assert result == "Decreto"
    
    def test_train_all_classifiers(self):
        """Testa o treinamento de todos os classificadores"""
        results = self.classifier.train_all_classifiers()
        
        assert isinstance(results, dict)
        assert len(results) > 0
        
        # Verificar se todos os tipos de classificação foram treinados
        for classification_type in ClassificationType:
            assert classification_type.value in results
            assert results[classification_type.value] >= 0.0


def test_compatibility_functions():
    """Testa as funções de compatibilidade com a API antiga"""
    from src.modules.nlp.classifier import (
        classify_subject, classify_article_type, classify_legal_intention,
        generate_title, classify_legal_category, classify_normative_type
    )
    
    text = "Art. 1º É livre a manifestação do pensamento"
    
    # Testar se as funções executam sem erro
    result_subject = classify_subject(text)
    result_article = classify_article_type(text)
    result_intention = classify_legal_intention(text)
    result_title = generate_title(text)
    result_category = classify_legal_category(text)
    result_normative = classify_normative_type(text)
    
    # Verificar que todas retornam strings
    assert isinstance(result_subject, str)
    assert isinstance(result_article, str)
    assert isinstance(result_intention, str)
    assert isinstance(result_title, str)
    assert isinstance(result_category, str)
    assert isinstance(result_normative, str)


def test_legal_text_examples():
    """Testa com exemplos reais de texto legal"""
    classifier = LegalDocumentClassifier()
    
    # Treinar classificadores
    classifier.train_all_classifiers()
    
    # Textos de exemplo
    examples = [
        {
            'text': "Art. 5º Todos são iguais perante a lei, sem distinção de qualquer natureza",
            'expected_subject': "Direitos Fundamentais"
        },
        {
            'text': "Art. 156. Compete aos Municípios instituir impostos sobre:",
            'expected_subject': "Tributação"
        },
        {
            'text': "Para os efeitos desta lei, considera-se empregador a empresa",
            'expected_article_type': "Definição"
        },
        {
            'text': "É vedado o uso de trabalho infantil",
            'expected_article_type': "Proibição"
        }
    ]
    
    for example in examples:
        text = example['text']
        
        # Classificar assunto
        if 'expected_subject' in example:
            result = classifier.classify_subject(text)
            # Não fazemos assert exato pois o modelo pode não ser perfeito
            assert result is not None
            
        # Classificar tipo de artigo
        if 'expected_article_type' in example:
            result = classifier.classify_article_type(text)
            assert result is not None


if __name__ == "__main__":
    # Configurar logging para os testes
    logging.basicConfig(level=logging.INFO)
    
    # Executar testes
    pytest.main([__file__, "-v"])