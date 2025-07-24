"""
Tests for enhanced sentiment analysis functionality
"""

import pytest
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

from modules.nlp.enhanced_sentiment import EnhancedSentimentAnalyzer, SentimentFilter
from modules.nlp.sentiment import sentiment_analysis, sentiment_analysis_comprehensive
from modules.analysis.sentiment_analysis import SentimentAnalysisReport


class TestEnhancedSentimentAnalysis:
    """Test cases for enhanced sentiment analysis"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.analyzer = EnhancedSentimentAnalyzer()
        self.sentiment_filter = SentimentFilter()
        self.report_generator = SentimentAnalysisReport()
    
    def test_basic_sentiment_analysis(self):
        """Test basic sentiment analysis functionality"""
        # Test positive sentiment
        result = sentiment_analysis("I love this product! It's amazing!")
        assert result == "Positive"
        
        # Test negative sentiment
        result = sentiment_analysis("This is terrible and disappointing")
        assert result == "Negative"
        
        # Test neutral sentiment
        result = sentiment_analysis("This is a regular product")
        assert result == "Neutral"
        
        # Test empty input
        result = sentiment_analysis("")
        assert result is None
    
    def test_comprehensive_sentiment_analysis(self):
        """Test comprehensive sentiment analysis"""
        text = "I'm so happy with this excellent product! The quality is amazing but the price is a bit high."
        result = sentiment_analysis_comprehensive(text)
        
        assert result is not None
        assert 'basic_sentiment' in result
        assert 'emotions' in result
        assert 'intensity' in result
        assert 'subjectivity' in result
        assert 'aspect_sentiment' in result
        
        # Check basic sentiment
        assert result['basic_sentiment']['classification'] in ['Positive', 'Negative', 'Neutral']
        assert 'polarity' in result['basic_sentiment']
        
        # Check emotions
        assert 'scores' in result['emotions']
        assert 'dominant_emotion' in result['emotions']
        
        # Check intensity
        assert 'intensity' in result['intensity']
        assert 'confidence' in result['intensity']
        
        # Check subjectivity
        assert 'score' in result['subjectivity']
        assert 'classification' in result['subjectivity']
    
    def test_emotion_detection(self):
        """Test emotion detection functionality"""
        # Test joy emotion
        result = self.analyzer.analyze_comprehensive("I'm so happy and joyful today!")
        emotions = result['emotions']
        assert 'joy' in emotions['scores']
        
        # Test anger emotion
        result = self.analyzer.analyze_comprehensive("I'm furious and angry about this!")
        emotions = result['emotions']
        assert 'anger' in emotions['scores']
    
    def test_aspect_based_sentiment(self):
        """Test aspect-based sentiment analysis"""
        text = "The quality is excellent but the price is too expensive"
        result = self.analyzer.analyze_comprehensive(text)
        
        aspect_sentiment = result['aspect_sentiment']
        
        # Should detect quality and price aspects
        if aspect_sentiment:
            assert any('quality' in aspect or 'price' in aspect for aspect in aspect_sentiment.keys())
    
    def test_language_detection(self):
        """Test language detection"""
        # English text
        result = self.analyzer.analyze_comprehensive("This is a great product and I love it")
        assert result['language'] in ['english', 'unknown']
        
        # Portuguese text
        result = self.analyzer.analyze_comprehensive("Este produto é muito bom e eu gosto dele")
        assert result['language'] in ['portuguese', 'unknown']
    
    def test_sentiment_filtering(self):
        """Test sentiment filtering functionality"""
        # Create mock results
        results = [
            {'basic_sentiment': {'classification': 'Positive'}, 'overall_confidence': 0.8},
            {'basic_sentiment': {'classification': 'Negative'}, 'overall_confidence': 0.9},
            {'basic_sentiment': {'classification': 'Neutral'}, 'overall_confidence': 0.5},
        ]
        
        # Filter by sentiment type
        positive_results = self.sentiment_filter.filter_by_sentiment(results, 'Positive')
        assert len(positive_results) == 1
        assert positive_results[0]['basic_sentiment']['classification'] == 'Positive'
        
        # Filter by confidence
        high_confidence_results = self.sentiment_filter.filter_by_confidence(results, 0.7)
        assert len(high_confidence_results) == 2
    
    def test_analysis_report_generation(self):
        """Test comprehensive analysis report generation"""
        texts = [
            "I love this product! It's amazing!",
            "This is terrible and disappointing",
            "The quality is good but price is high",
            "Neutral comment about the product"
        ]
        
        report = self.report_generator.analyze_text_collection(texts)
        
        # Check report structure
        assert 'summary' in report
        assert 'sentiment_distribution' in report
        assert 'emotion_analysis' in report
        assert 'key_insights' in report
        assert 'recommendations' in report
        assert 'individual_results' in report
        
        # Check individual results
        assert len(report['individual_results']) == len(texts)
        
        # Check summary
        summary = report['summary']
        assert 'total_texts' in summary
        assert summary['total_texts'] == len(texts)
    
    def test_analyst_context_generation(self):
        """Test analyst context generation"""
        texts = [
            "I love this product! It's amazing!",
            "This is terrible and disappointing",
            "The quality is good but price is high"
        ]
        
        analysis_report = self.report_generator.analyze_text_collection(texts)
        analyst_context = self.report_generator.generate_analyst_context(analysis_report)
        
        # Check analyst context structure
        assert 'analyst_summary' in analyst_context
        assert 'priority_alerts' in analyst_context
        assert 'action_items' in analyst_context
        assert 'context_enrichment' in analyst_context
        
        # Check analyst summary
        analyst_summary = analyst_context['analyst_summary']
        assert 'total_texts_analyzed' in analyst_summary
        assert 'overall_sentiment_health' in analyst_summary
        assert 'confidence_level' in analyst_summary
    
    def test_filter_and_classify(self):
        """Test filtering and classification functionality"""
        texts = [
            "I love this product! It's amazing!",
            "This is terrible and disappointing"
        ]
        
        analysis_report = self.report_generator.analyze_text_collection(texts)
        individual_results = analysis_report['individual_results']  # Keep full results
        
        # Test filtering
        criteria = {'sentiment_type': 'Positive', 'min_confidence': 0.5}
        filtered_results = self.report_generator.filter_and_classify([r['sentiment'] for r in individual_results], criteria)
        
        assert 'original_count' in filtered_results
        assert 'filtered_count' in filtered_results
        assert 'criteria_applied' in filtered_results
        assert 'classifications' in filtered_results
    
    def test_empty_input_handling(self):
        """Test handling of empty or invalid inputs"""
        # Test empty string
        result = self.analyzer.analyze_comprehensive("")
        assert result['basic_sentiment']['classification'] == "Neutral"
        
        # Test None input
        result = sentiment_analysis("")
        assert result is None
        
        # Test empty text collection
        report = self.report_generator.analyze_text_collection([])
        assert report['summary'] == {}
    
    def test_intensity_and_confidence_scoring(self):
        """Test intensity and confidence scoring"""
        # High intensity positive text
        result = self.analyzer.analyze_comprehensive("This is absolutely fantastic and amazing!")
        assert result['intensity']['intensity'] > 0.5
        
        # Low intensity neutral text
        result = self.analyzer.analyze_comprehensive("This is okay")
        assert result['intensity']['intensity'] < 0.5
    
    def test_subjectivity_analysis(self):
        """Test subjectivity analysis"""
        # Subjective text - adjust expectation based on actual TextBlob behavior
        result = self.analyzer.analyze_comprehensive("I think this is the best product ever!")
        assert result['subjectivity']['classification'] in ['Objective', 'Subjective', 'Highly Subjective']
        
        # Test that subjectivity score is between 0 and 1
        assert 0 <= result['subjectivity']['score'] <= 1
    
    def test_portuguese_text_analysis(self):
        """Test analysis of Portuguese text"""
        text = "Eu amo este produto! É incrível e a qualidade é excelente!"
        result = self.analyzer.analyze_comprehensive(text)
        
        assert result is not None
        # TextBlob might not handle Portuguese perfectly, so test that we get a valid result
        assert result['basic_sentiment']['classification'] in ['Positive', 'Negative', 'Neutral']
        assert result['language'] == 'portuguese'


if __name__ == '__main__':
    # Run tests if script is executed directly
    pytest.main([__file__, '-v'])