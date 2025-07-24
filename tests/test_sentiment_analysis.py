"""
Testes para o módulo de análise de sentimento em português.
"""

import unittest
import sys
import os

# Adicionar o diretório do projeto ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.modules.analysis.sentiment_analysis import (
    sentiment_analysis, sentiment_tags, sentiment_noun_phrases,
    sentiment_sentenses, sentiment_words, sentiment_words_sigularize,
    sentiment_words_pluralize, sentiment_lemmarize, sentiment_verb
)


class TestSentimentAnalysis(unittest.TestCase):
    """Testes para análise de sentimento"""

    def test_sentiment_analysis_positive(self):
        """Testa classificação de sentimento positivo"""
        result = sentiment_analysis("I love this product!")
        self.assertEqual(result, "Positivo")

    def test_sentiment_analysis_negative(self):
        """Testa classificação de sentimento negativo"""
        result = sentiment_analysis("This product is terrible")
        self.assertEqual(result, "Negativo")

    def test_sentiment_analysis_neutral(self):
        """Testa classificação de sentimento neutro"""
        result = sentiment_analysis("This is a product")
        self.assertEqual(result, "Neutro")

    def test_sentiment_analysis_empty_text(self):
        """Testa comportamento com texto vazio"""
        result = sentiment_analysis("")
        self.assertIsNone(result)

    def test_sentiment_analysis_return_types(self):
        """Testa se os tipos de retorno estão corretos"""
        # Testa se retorna strings em português
        positive_result = sentiment_analysis("Amazing product!")
        negative_result = sentiment_analysis("Horrible experience")
        neutral_result = sentiment_analysis("This is text")
        
        self.assertIn(positive_result, ["Positivo", "Negativo", "Neutro"])
        self.assertIn(negative_result, ["Positivo", "Negativo", "Neutro"])
        self.assertIn(neutral_result, ["Positivo", "Negativo", "Neutro"])

    def test_sentiment_words(self):
        """Testa extração de palavras"""
        result = sentiment_words("Hello world")
        self.assertIsNotNone(result)
        self.assertTrue(len(result) > 0)

    def test_sentiment_words_empty(self):
        """Testa extração de palavras com texto vazio"""
        result = sentiment_words("")
        self.assertIsNone(result)

    def test_sentiment_lemmarize(self):
        """Testa lematização de palavras"""
        result = sentiment_lemmarize("running")
        self.assertIsNotNone(result)

    def test_sentiment_verb(self):
        """Testa lematização de verbos"""
        result = sentiment_verb("running")
        self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main()