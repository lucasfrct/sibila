# Enhanced Sentiment Analysis Module
# Provides multi-dimensional sentiment analysis with emotion detection,
# intensity scoring, subjectivity analysis, and aspect-based sentiment

from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import Dict, List, Optional, Tuple
import re
import nltk
from collections import defaultdict


class EnhancedSentimentAnalyzer:
    """
    Enhanced sentiment analyzer with multiple dimensions:
    - Basic sentiment (positive, negative, neutral)
    - Emotion detection (joy, anger, fear, sadness, surprise, disgust)
    - Intensity and confidence scores
    - Subjectivity analysis
    - Aspect-based sentiment analysis
    """
    
    def __init__(self):
        self.vader_analyzer = SentimentIntensityAnalyzer()
        
        # Emotion lexicon for Portuguese and English
        self.emotion_lexicon = {
            'joy': ['feliz', 'alegre', 'contente', 'eufórico', 'radiante', 'happy', 'joyful', 'cheerful', 'delighted', 'elated'],
            'anger': ['raiva', 'irritado', 'furioso', 'irado', 'bravo', 'angry', 'furious', 'mad', 'irritated', 'annoyed'],
            'fear': ['medo', 'assustado', 'amedrontado', 'temeroso', 'ansioso', 'afraid', 'scared', 'fearful', 'anxious', 'worried'],
            'sadness': ['triste', 'melancólico', 'deprimido', 'abatido', 'triste', 'sad', 'depressed', 'melancholy', 'gloomy', 'sorrowful'],
            'surprise': ['surpreso', 'espantado', 'atônito', 'pasmo', 'chocado', 'surprised', 'amazed', 'astonished', 'shocked', 'stunned'],
            'disgust': ['nojo', 'repugnância', 'aversão', 'repulsa', 'asco', 'disgusted', 'repulsed', 'revolted', 'sickened', 'appalled']
        }
        
        # Aspect keywords for aspect-based sentiment analysis
        self.aspect_keywords = {
            'quality': ['qualidade', 'quality', 'bom', 'ruim', 'good', 'bad', 'excelente', 'excellent', 'péssimo', 'terrible'],
            'price': ['preço', 'price', 'caro', 'barato', 'expensive', 'cheap', 'custo', 'cost', 'valor', 'value'],
            'service': ['atendimento', 'service', 'serviço', 'staff', 'funcionário', 'employee', 'suporte', 'support'],
            'delivery': ['entrega', 'delivery', 'envio', 'shipping', 'prazo', 'deadline', 'rápido', 'fast', 'lento', 'slow'],
            'product': ['produto', 'product', 'item', 'mercadoria', 'goods', 'artigo', 'article']
        }
    
    def analyze_comprehensive(self, text: str) -> Dict:
        """
        Perform comprehensive sentiment analysis with multiple dimensions
        
        Args:
            text (str): Text to analyze
            
        Returns:
            Dict: Comprehensive analysis results
        """
        if not text or text.strip() == "":
            return self._empty_result()
        
        # Basic sentiment analysis
        basic_sentiment = self._analyze_basic_sentiment(text)
        
        # Emotion detection
        emotions = self._detect_emotions(text)
        
        # Intensity and confidence
        intensity_scores = self._analyze_intensity(text)
        
        # Subjectivity analysis
        subjectivity = self._analyze_subjectivity(text)
        
        # Aspect-based sentiment
        aspect_sentiment = self._analyze_aspect_sentiment(text)
        
        # Language detection
        language = self._detect_language(text)
        
        return {
            'text': text,
            'language': language,
            'basic_sentiment': basic_sentiment,
            'emotions': emotions,
            'intensity': intensity_scores,
            'subjectivity': subjectivity,
            'aspect_sentiment': aspect_sentiment,
            'overall_confidence': self._calculate_overall_confidence(basic_sentiment, emotions, intensity_scores)
        }
    
    def _analyze_basic_sentiment(self, text: str) -> Dict:
        """Analyze basic sentiment using both TextBlob and VADER"""
        # TextBlob analysis
        blob = TextBlob(text)
        textblob_polarity = blob.sentiment.polarity
        
        # VADER analysis
        vader_scores = self.vader_analyzer.polarity_scores(text)
        
        # Combine results
        combined_polarity = (textblob_polarity + vader_scores['compound']) / 2
        
        if combined_polarity > 0.1:
            classification = "Positive"
        elif combined_polarity < -0.1:
            classification = "Negative"
        else:
            classification = "Neutral"
        
        return {
            'classification': classification,
            'polarity': combined_polarity,
            'textblob_polarity': textblob_polarity,
            'vader_compound': vader_scores['compound'],
            'vader_details': {
                'positive': vader_scores['pos'],
                'neutral': vader_scores['neu'],
                'negative': vader_scores['neg']
            }
        }
    
    def _detect_emotions(self, text: str) -> Dict:
        """Detect emotions in text based on emotion lexicon"""
        text_lower = text.lower()
        emotion_scores = defaultdict(int)
        
        for emotion, keywords in self.emotion_lexicon.items():
            for keyword in keywords:
                # Count occurrences of emotion keywords
                count = len(re.findall(r'\b' + re.escape(keyword) + r'\b', text_lower))
                emotion_scores[emotion] += count
        
        # Normalize scores
        total_words = len(text.split())
        if total_words > 0:
            for emotion in emotion_scores:
                emotion_scores[emotion] = emotion_scores[emotion] / total_words
        
        # Find dominant emotion
        dominant_emotion = max(emotion_scores.items(), key=lambda x: x[1]) if emotion_scores else ("neutral", 0)
        
        return {
            'scores': dict(emotion_scores),
            'dominant_emotion': dominant_emotion[0],
            'dominant_score': dominant_emotion[1]
        }
    
    def _analyze_intensity(self, text: str) -> Dict:
        """Analyze sentiment intensity and confidence"""
        blob = TextBlob(text)
        vader_scores = self.vader_analyzer.polarity_scores(text)
        
        # Calculate intensity based on polarity magnitude
        textblob_intensity = abs(blob.sentiment.polarity)
        vader_intensity = abs(vader_scores['compound'])
        
        # Average intensity
        avg_intensity = (textblob_intensity + vader_intensity) / 2
        
        # Confidence based on agreement between methods
        agreement = 1 - abs(blob.sentiment.polarity - vader_scores['compound']) / 2
        
        return {
            'intensity': avg_intensity,
            'confidence': agreement,
            'textblob_intensity': textblob_intensity,
            'vader_intensity': vader_intensity
        }
    
    def _analyze_subjectivity(self, text: str) -> Dict:
        """Analyze subjectivity (objective vs subjective)"""
        blob = TextBlob(text)
        subjectivity = blob.sentiment.subjectivity
        
        if subjectivity > 0.6:
            classification = "Highly Subjective"
        elif subjectivity > 0.3:
            classification = "Subjective"
        else:
            classification = "Objective"
        
        return {
            'score': subjectivity,
            'classification': classification
        }
    
    def _analyze_aspect_sentiment(self, text: str) -> Dict:
        """Perform aspect-based sentiment analysis"""
        text_lower = text.lower()
        aspect_sentiments = {}
        
        for aspect, keywords in self.aspect_keywords.items():
            # Check if aspect is mentioned
            aspect_mentioned = any(keyword in text_lower for keyword in keywords)
            
            if aspect_mentioned:
                # Extract sentences containing aspect keywords
                sentences = text.split('.')
                relevant_sentences = []
                
                for sentence in sentences:
                    if any(keyword in sentence.lower() for keyword in keywords):
                        relevant_sentences.append(sentence.strip())
                
                if relevant_sentences:
                    # Analyze sentiment of relevant sentences
                    combined_text = ' '.join(relevant_sentences)
                    blob = TextBlob(combined_text)
                    polarity = blob.sentiment.polarity
                    
                    if polarity > 0.1:
                        sentiment = "Positive"
                    elif polarity < -0.1:
                        sentiment = "Negative"
                    else:
                        sentiment = "Neutral"
                    
                    aspect_sentiments[aspect] = {
                        'sentiment': sentiment,
                        'polarity': polarity,
                        'relevant_text': combined_text
                    }
        
        return aspect_sentiments
    
    def _detect_language(self, text: str) -> str:
        """Detect language of the text (simple heuristic)"""
        portuguese_words = ['de', 'da', 'do', 'das', 'dos', 'em', 'na', 'no', 'nas', 'nos', 'com', 'por', 'para', 'é', 'são', 'que', 'não', 'uma', 'um']
        english_words = ['the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'a', 'an']
        
        text_lower = text.lower()
        words = text_lower.split()
        
        pt_count = sum(1 for word in words if word in portuguese_words)
        en_count = sum(1 for word in words if word in english_words)
        
        if pt_count > en_count:
            return "portuguese"
        elif en_count > pt_count:
            return "english"
        else:
            return "unknown"
    
    def _calculate_overall_confidence(self, basic_sentiment: Dict, emotions: Dict, intensity: Dict) -> float:
        """Calculate overall confidence score"""
        base_confidence = intensity.get('confidence', 0)
        emotion_confidence = min(emotions.get('dominant_score', 0) * 10, 1)  # Scale emotion score
        intensity_confidence = intensity.get('intensity', 0)
        
        return (base_confidence + emotion_confidence + intensity_confidence) / 3
    
    def _empty_result(self) -> Dict:
        """Return empty result structure for invalid input"""
        return {
            'text': "",
            'language': "unknown",
            'basic_sentiment': {'classification': "Neutral", 'polarity': 0},
            'emotions': {'scores': {}, 'dominant_emotion': "neutral", 'dominant_score': 0},
            'intensity': {'intensity': 0, 'confidence': 0},
            'subjectivity': {'score': 0, 'classification': "Objective"},
            'aspect_sentiment': {},
            'overall_confidence': 0
        }


class SentimentFilter:
    """
    Filtering utilities for sentiment analysis results
    """
    
    @staticmethod
    def filter_by_sentiment(results: List[Dict], sentiment_type: str) -> List[Dict]:
        """Filter results by sentiment type (Positive, Negative, Neutral)"""
        return [r for r in results if r.get('basic_sentiment', {}).get('classification') == sentiment_type]
    
    @staticmethod
    def filter_by_emotion(results: List[Dict], emotion: str) -> List[Dict]:
        """Filter results by dominant emotion"""
        return [r for r in results if r.get('emotions', {}).get('dominant_emotion') == emotion]
    
    @staticmethod
    def filter_by_confidence(results: List[Dict], min_confidence: float) -> List[Dict]:
        """Filter results by minimum confidence score"""
        return [r for r in results if r.get('overall_confidence', 0) >= min_confidence]
    
    @staticmethod
    def filter_by_intensity(results: List[Dict], min_intensity: float) -> List[Dict]:
        """Filter results by minimum intensity"""
        return [r for r in results if r.get('intensity', {}).get('intensity', 0) >= min_intensity]
    
    @staticmethod
    def filter_by_subjectivity(results: List[Dict], subjectivity_type: str) -> List[Dict]:
        """Filter results by subjectivity type (Objective, Subjective, Highly Subjective)"""
        return [r for r in results if r.get('subjectivity', {}).get('classification') == subjectivity_type]
    
    @staticmethod
    def filter_by_aspect(results: List[Dict], aspect: str) -> List[Dict]:
        """Filter results by specific aspect presence"""
        return [r for r in results if aspect in r.get('aspect_sentiment', {})]


# Backward compatibility functions
def sentiment_analysis_enhanced(text: str = "") -> Dict:
    """Enhanced sentiment analysis with comprehensive results"""
    analyzer = EnhancedSentimentAnalyzer()
    return analyzer.analyze_comprehensive(text)


def sentiment_classification_only(text: str = "") -> str:
    """Return only the basic sentiment classification for backward compatibility"""
    if text == "":
        return "Neutral"
    
    analyzer = EnhancedSentimentAnalyzer()
    result = analyzer.analyze_comprehensive(text)
    return result['basic_sentiment']['classification']