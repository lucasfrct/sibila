
"""
Módulo de análise de sentimento em português.

Este módulo fornece funcionalidades para análise de sentimento de textos em português,
incluindo classificação de polaridade, extração de tags, frases nominais, sentenças,
palavras e operações de lematização.
"""

from textblob import TextBlob
from textblob import Word


def sentiment_analysis(text: str = "") -> str:
    """
    Analisa o sentimento de um texto e retorna a classificação em português.
    
    Args:
        text (str): O texto para análise de sentimento. Padrão é string vazia.
        
    Returns:
        str: Classificação do sentimento ("Positivo", "Negativo", "Neutro") ou None se texto vazio.
        
    Example:
        >>> sentiment_analysis("Eu amo este produto!")
        "Positivo"
        >>> sentiment_analysis("Este produto é terrível")
        "Negativo"
    """
    if text == "":
        return None

    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0:
        return "Positivo"

    if polarity < 0:
        return "Negativo"

    return "Neutro"


def sentiment_tags(text: str = ""):
    """
    Extrai as tags de partes do discurso de um texto.
    
    Args:
        text (str): O texto para extração de tags. Padrão é string vazia.
        
    Returns:
        list: Lista de tags de partes do discurso ou None se texto vazio.
    """
    if text == "":
        return None

    blob = TextBlob(text)
    return blob.tags


def sentiment_noun_phrases(text: str = ""):
    """
    Extrai as frases nominais de um texto.
    
    Args:
        text (str): O texto para extração de frases nominais. Padrão é string vazia.
        
    Returns:
        list: Lista de frases nominais ou None se texto vazio.
    """
    if text == "":
        return None

    blob = TextBlob(text)
    return blob.noun_phrases


def sentiment_sentenses(text: str = ""):
    """
    Divide o texto em sentenças.
    
    Args:
        text (str): O texto para divisão em sentenças. Padrão é string vazia.
        
    Returns:
        list: Lista de sentenças ou None se texto vazio.
    """
    if text == "":
        return None

    blob = TextBlob(text)
    return blob.sentences


def sentiment_words(text: str = ""):
    """
    Extrai as palavras de um texto.
    
    Args:
        text (str): O texto para extração de palavras. Padrão é string vazia.
        
    Returns:
        list: Lista de palavras ou None se texto vazio.
    """
    if text == "":
        return None

    blob = TextBlob(text)
    return blob.words


def sentiment_words_sigularize(text: str = ""):
    """
    Singulariza todas as palavras de um texto.
    
    Args:
        text (str): O texto para singularização das palavras. Padrão é string vazia.
        
    Returns:
        list: Lista de palavras singularizadas ou None se texto vazio.
    """
    if text == "":
        return None

    blob = TextBlob(text)

    words = []
    for word in blob.words:
        words.append(word.singularize())
    return words


def sentiment_words_pluralize(text: str = ""):
    """
    Pluraliza todas as palavras de um texto.
    
    Args:
        text (str): O texto para pluralização das palavras. Padrão é string vazia.
        
    Returns:
        list: Lista de palavras pluralizadas ou None se texto vazio.
    """
    if text == "":
        return None

    blob = TextBlob(text)

    words = []
    for word in blob.words:
        words.append(word.pluralize())
    return words


def sentiment_lemmarize(text: str = ""):
    """
    Lematiza uma palavra (reduz à sua forma base).
    
    Args:
        text (str): A palavra para lematização.
        
    Returns:
        str: Palavra lematizada.
    """
    w = Word(text)
    return w.lemmatize()


def sentiment_verb(text: str = ""):
    """
    Lematiza uma palavra como verbo.
    
    Args:
        text (str): A palavra para lematização como verbo.
        
    Returns:
        str: Verbo lematizado.
    """
    w = Word(text)
    return w.lemmatize("v")
# Enhanced Analysis Module for Sentiment Analysis
# Provides enriched context for analysts with comprehensive sentiment insights

from typing import Dict, List, Optional, Tuple, Any
from collections import defaultdict, Counter
import json
from datetime import datetime

from ..nlp.enhanced_sentiment import EnhancedSentimentAnalyzer, SentimentFilter


class SentimentAnalysisReport:
    """
    Comprehensive sentiment analysis reporting for analysts
    Provides enriched context and insights from sentiment data
    """
    
    def __init__(self):
        self.sentiment_analyzer = EnhancedSentimentAnalyzer()
        self.sentiment_filter = SentimentFilter()
    
    def analyze_text_collection(self, texts: List[str], metadata: Optional[List[Dict]] = None) -> Dict:
        """
        Analyze a collection of texts and provide comprehensive insights
        
        Args:
            texts (List[str]): Collection of texts to analyze
            metadata (Optional[List[Dict]]): Optional metadata for each text
            
        Returns:
            Dict: Comprehensive analysis report
        """
        if not texts:
            return self._empty_report()
        
        # Analyze each text
        individual_results = []
        for i, text in enumerate(texts):
            sentiment_result = self.sentiment_analyzer.analyze_comprehensive(text)
            
            combined_result = {
                'index': i,
                'text': text,
                'sentiment': sentiment_result,
                'metadata': metadata[i] if metadata and i < len(metadata) else {}
            }
            individual_results.append(combined_result)
        
        # Generate comprehensive report
        report = {
            'summary': self._generate_summary(individual_results),
            'sentiment_distribution': self._analyze_sentiment_distribution(individual_results),
            'emotion_analysis': self._analyze_emotions(individual_results),
            'aspect_insights': self._analyze_aspects(individual_results),
            'language_distribution': self._analyze_languages(individual_results),
            'quality_metrics': self._calculate_quality_metrics(individual_results),
            'key_insights': self._extract_key_insights(individual_results),
            'recommendations': self._generate_recommendations(individual_results),
            'individual_results': individual_results,
            'generated_at': datetime.now().isoformat()
        }
        
        return report
    
    def filter_and_classify(self, analysis_results: List[Dict], criteria: Dict) -> Dict:
        """
        Filter and classify analysis results based on criteria
        
        Args:
            analysis_results (List[Dict]): Results from sentiment analysis
            criteria (Dict): Filtering and classification criteria
            
        Returns:
            Dict: Filtered and classified results
        """
        filtered_results = analysis_results.copy()
        
        # Apply filters
        if 'sentiment_type' in criteria:
            filtered_results = self.sentiment_filter.filter_by_sentiment(
                filtered_results, criteria['sentiment_type']
            )
        
        if 'min_confidence' in criteria:
            filtered_results = self.sentiment_filter.filter_by_confidence(
                filtered_results, criteria['min_confidence']
            )
        
        if 'emotion' in criteria:
            filtered_results = self.sentiment_filter.filter_by_emotion(
                filtered_results, criteria['emotion']
            )
        
        if 'min_intensity' in criteria:
            filtered_results = self.sentiment_filter.filter_by_intensity(
                filtered_results, criteria['min_intensity']
            )
        
        if 'subjectivity_type' in criteria:
            filtered_results = self.sentiment_filter.filter_by_subjectivity(
                filtered_results, criteria['subjectivity_type']
            )
        
        if 'aspect' in criteria:
            filtered_results = self.sentiment_filter.filter_by_aspect(
                filtered_results, criteria['aspect']
            )
        
        # Classify results
        classifications = self._classify_results(filtered_results)
        
        return {
            'original_count': len(analysis_results),
            'filtered_count': len(filtered_results),
            'criteria_applied': criteria,
            'classifications': classifications,
            'filtered_results': filtered_results
        }
    
    def generate_analyst_context(self, analysis_report: Dict) -> Dict:
        """
        Generate enriched context specifically for analysts
        
        Args:
            analysis_report (Dict): Analysis report from analyze_text_collection
            
        Returns:
            Dict: Enriched analyst context
        """
        summary = analysis_report.get('summary', {})
        individual_results = analysis_report.get('individual_results', [])
        
        # Priority alerts
        alerts = self._generate_priority_alerts(individual_results)
        
        # Trend analysis
        trends = self._analyze_trends(individual_results)
        
        # Outlier detection
        outliers = self._detect_outliers(individual_results)
        
        # Comparative analysis
        comparative = self._generate_comparative_analysis(individual_results)
        
        # Action items
        action_items = self._generate_action_items(individual_results, alerts)
        
        return {
            'analyst_summary': {
                'total_texts_analyzed': len(individual_results),
                'overall_sentiment_health': self._calculate_sentiment_health(summary),
                'confidence_level': summary.get('average_confidence', 0),
                'key_concerns': alerts.get('high_priority', []),
                'opportunities': alerts.get('opportunities', [])
            },
            'priority_alerts': alerts,
            'trend_analysis': trends,
            'outlier_detection': outliers,
            'comparative_analysis': comparative,
            'action_items': action_items,
            'context_enrichment': {
                'sentiment_patterns': self._identify_sentiment_patterns(individual_results),
                'emotional_drivers': self._identify_emotional_drivers(individual_results),
                'aspect_performance': self._analyze_aspect_performance(individual_results)
            }
        }
    
    def _generate_summary(self, results: List[Dict]) -> Dict:
        """Generate overall summary statistics"""
        if not results:
            return {}
        
        sentiments = [r['sentiment']['basic_sentiment']['classification'] for r in results]
        confidences = [r['sentiment']['overall_confidence'] for r in results]
        intensities = [r['sentiment']['intensity']['intensity'] for r in results]
        
        return {
            'total_texts': len(results),
            'sentiment_counts': Counter(sentiments),
            'average_confidence': sum(confidences) / len(confidences),
            'average_intensity': sum(intensities) / len(intensities),
            'confidence_distribution': {
                'high': len([c for c in confidences if c > 0.7]),
                'medium': len([c for c in confidences if 0.3 <= c <= 0.7]),
                'low': len([c for c in confidences if c < 0.3])
            }
        }
    
    def _analyze_sentiment_distribution(self, results: List[Dict]) -> Dict:
        """Analyze sentiment distribution patterns"""
        sentiments = [r['sentiment']['basic_sentiment'] for r in results]
        
        positive_count = len([s for s in sentiments if s['classification'] == 'Positive'])
        negative_count = len([s for s in sentiments if s['classification'] == 'Negative'])
        neutral_count = len([s for s in sentiments if s['classification'] == 'Neutral'])
        total = len(sentiments)
        
        if total == 0:
            return {}
        
        return {
            'distribution': {
                'positive': {'count': positive_count, 'percentage': (positive_count / total) * 100},
                'negative': {'count': negative_count, 'percentage': (negative_count / total) * 100},
                'neutral': {'count': neutral_count, 'percentage': (neutral_count / total) * 100}
            },
            'polarity_stats': {
                'average': sum([s['polarity'] for s in sentiments]) / total,
                'max': max([s['polarity'] for s in sentiments]),
                'min': min([s['polarity'] for s in sentiments])
            }
        }
    
    def _analyze_emotions(self, results: List[Dict]) -> Dict:
        """Analyze emotion patterns across texts"""
        all_emotions = defaultdict(list)
        dominant_emotions = []
        
        for result in results:
            emotions = result['sentiment']['emotions']
            dominant_emotions.append(emotions['dominant_emotion'])
            
            for emotion, score in emotions['scores'].items():
                all_emotions[emotion].append(score)
        
        # Calculate averages
        emotion_averages = {}
        for emotion, scores in all_emotions.items():
            if scores:
                emotion_averages[emotion] = sum(scores) / len(scores)
        
        return {
            'dominant_emotion_distribution': Counter(dominant_emotions),
            'emotion_averages': emotion_averages,
            'most_prevalent_emotion': max(emotion_averages.items(), key=lambda x: x[1]) if emotion_averages else ('neutral', 0)
        }
    
    def _analyze_aspects(self, results: List[Dict]) -> Dict:
        """Analyze aspect-based sentiment patterns"""
        aspect_sentiments = defaultdict(list)
        
        for result in results:
            aspects = result['sentiment']['aspect_sentiment']
            for aspect, details in aspects.items():
                aspect_sentiments[aspect].append(details)
        
        aspect_analysis = {}
        for aspect, sentiments in aspect_sentiments.items():
            if sentiments:
                sentiment_counts = Counter([s['sentiment'] for s in sentiments])
                avg_polarity = sum([s['polarity'] for s in sentiments]) / len(sentiments)
                
                aspect_analysis[aspect] = {
                    'total_mentions': len(sentiments),
                    'sentiment_distribution': sentiment_counts,
                    'average_polarity': avg_polarity,
                    'overall_sentiment': 'Positive' if avg_polarity > 0.1 else 'Negative' if avg_polarity < -0.1 else 'Neutral'
                }
        
        return aspect_analysis
    
    def _analyze_languages(self, results: List[Dict]) -> Dict:
        """Analyze language distribution"""
        languages = [r['sentiment']['language'] for r in results]
        return {
            'distribution': Counter(languages),
            'total_languages': len(set(languages))
        }
    
    def _calculate_quality_metrics(self, results: List[Dict]) -> Dict:
        """Calculate quality metrics for the analysis"""
        confidences = [r['sentiment']['overall_confidence'] for r in results]
        intensities = [r['sentiment']['intensity']['intensity'] for r in results]
        
        return {
            'data_quality_score': sum(confidences) / len(confidences) if confidences else 0,
            'analysis_reliability': len([c for c in confidences if c > 0.7]) / len(confidences) if confidences else 0,
            'signal_strength': sum(intensities) / len(intensities) if intensities else 0
        }
    
    def _extract_key_insights(self, results: List[Dict]) -> List[str]:
        """Extract key insights from the analysis"""
        insights = []
        
        # Sentiment insights
        sentiments = [r['sentiment']['basic_sentiment']['classification'] for r in results]
        sentiment_counter = Counter(sentiments)
        most_common_sentiment = sentiment_counter.most_common(1)[0] if sentiments else None
        
        if most_common_sentiment:
            percentage = (most_common_sentiment[1] / len(sentiments)) * 100
            insights.append(f"Dominant sentiment is {most_common_sentiment[0]} ({percentage:.1f}% of texts)")
        
        # Emotion insights
        emotions = [r['sentiment']['emotions']['dominant_emotion'] for r in results]
        emotion_counter = Counter(emotions)
        most_common_emotion = emotion_counter.most_common(1)[0] if emotions else None
        
        if most_common_emotion and most_common_emotion[0] != 'neutral':
            insights.append(f"Primary emotion detected: {most_common_emotion[0]}")
        
        # Confidence insights
        confidences = [r['sentiment']['overall_confidence'] for r in results]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        
        if avg_confidence > 0.8:
            insights.append("High confidence in analysis results")
        elif avg_confidence < 0.5:
            insights.append("Analysis confidence is below average - consider reviewing data quality")
        
        return insights
    
    def _generate_recommendations(self, results: List[Dict]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Analyze negative sentiment patterns
        negative_results = [r for r in results if r['sentiment']['basic_sentiment']['classification'] == 'Negative']
        if len(negative_results) > len(results) * 0.3:  # More than 30% negative
            recommendations.append("High negative sentiment detected - investigate root causes and implement improvement measures")
        
        # Analyze aspect-based issues
        aspect_issues = []
        for result in results:
            for aspect, details in result['sentiment']['aspect_sentiment'].items():
                if details['sentiment'] == 'Negative':
                    aspect_issues.append(aspect)
        
        if aspect_issues:
            common_issues = Counter(aspect_issues).most_common(3)
            for issue, count in common_issues:
                recommendations.append(f"Address {issue}-related concerns (mentioned negatively {count} times)")
        
        return recommendations
    
    def _classify_results(self, results: List[Dict]) -> Dict:
        """Classify filtered results into categories"""
        classifications = {
            'high_priority': [],
            'medium_priority': [],
            'low_priority': [],
            'positive_feedback': [],
            'issues_identified': []
        }
        
        for result in results:
            # Handle both formats: direct sentiment result or wrapped result
            if 'sentiment' in result:
                sentiment_data = result['sentiment']
            else:
                sentiment_data = result
            
            sentiment = sentiment_data['basic_sentiment']['classification']
            confidence = sentiment_data.get('overall_confidence', 0)
            intensity = sentiment_data.get('intensity', {}).get('intensity', 0)
            
            if sentiment == 'Negative' and confidence > 0.7:
                classifications['high_priority'].append(result)
            elif sentiment == 'Negative' and confidence > 0.5:
                classifications['medium_priority'].append(result)
            elif sentiment == 'Positive' and intensity > 0.6:
                classifications['positive_feedback'].append(result)
            
            # Check for specific issues in aspects
            aspect_sentiment = sentiment_data.get('aspect_sentiment', {})
            if aspect_sentiment:
                for aspect, details in aspect_sentiment.items():
                    if details['sentiment'] == 'Negative':
                        classifications['issues_identified'].append({
                            'result': result,
                            'issue_aspect': aspect,
                            'issue_details': details
                        })
        
        return classifications
    
    def _generate_priority_alerts(self, results: List[Dict]) -> Dict:
        """Generate priority alerts for analysts"""
        alerts = {
            'high_priority': [],
            'medium_priority': [],
            'opportunities': []
        }
        
        # High priority: High confidence negative sentiments
        for result in results:
            sentiment = result['sentiment']['basic_sentiment']
            if sentiment['classification'] == 'Negative' and result['sentiment']['overall_confidence'] > 0.8:
                alerts['high_priority'].append({
                    'text': result['text'][:100] + '...' if len(result['text']) > 100 else result['text'],
                    'reason': 'High confidence negative sentiment',
                    'confidence': result['sentiment']['overall_confidence'],
                    'polarity': sentiment['polarity']
                })
        
        # Opportunities: High confidence positive sentiments
        for result in results:
            sentiment = result['sentiment']['basic_sentiment']
            if sentiment['classification'] == 'Positive' and result['sentiment']['overall_confidence'] > 0.8:
                alerts['opportunities'].append({
                    'text': result['text'][:100] + '...' if len(result['text']) > 100 else result['text'],
                    'reason': 'Strong positive feedback opportunity',
                    'confidence': result['sentiment']['overall_confidence'],
                    'polarity': sentiment['polarity']
                })
        
        return alerts
    
    def _analyze_trends(self, results: List[Dict]) -> Dict:
        """Analyze trends in the data"""
        # This is a simplified trend analysis
        # In a real implementation, you'd want temporal data
        
        sentiments = [r['sentiment']['basic_sentiment']['polarity'] for r in results]
        confidences = [r['sentiment']['overall_confidence'] for r in results]
        
        return {
            'sentiment_trend': 'stable',  # Would need temporal data for real trends
            'confidence_trend': 'stable',
            'average_sentiment_polarity': sum(sentiments) / len(sentiments) if sentiments else 0,
            'average_confidence': sum(confidences) / len(confidences) if confidences else 0
        }
    
    def _detect_outliers(self, results: List[Dict]) -> List[Dict]:
        """Detect outlier results that need attention"""
        outliers = []
        
        # Calculate thresholds
        confidences = [r['sentiment']['overall_confidence'] for r in results]
        intensities = [r['sentiment']['intensity']['intensity'] for r in results]
        
        if confidences and intensities:
            avg_confidence = sum(confidences) / len(confidences)
            avg_intensity = sum(intensities) / len(intensities)
            
            for result in results:
                confidence = result['sentiment']['overall_confidence']
                intensity = result['sentiment']['intensity']['intensity']
                
                # Low confidence with high intensity (conflicting signals)
                if confidence < avg_confidence * 0.5 and intensity > avg_intensity * 1.5:
                    outliers.append({
                        'text': result['text'][:100] + '...' if len(result['text']) > 100 else result['text'],
                        'reason': 'Low confidence with high intensity - conflicting signals',
                        'confidence': confidence,
                        'intensity': intensity
                    })
        
        return outliers
    
    def _generate_comparative_analysis(self, results: List[Dict]) -> Dict:
        """Generate comparative analysis between different segments"""
        return {
            'positive_vs_negative': {
                'positive_count': len([r for r in results if r['sentiment']['basic_sentiment']['classification'] == 'Positive']),
                'negative_count': len([r for r in results if r['sentiment']['basic_sentiment']['classification'] == 'Negative']),
                'sentiment_ratio': 'positive_dominant' if len([r for r in results if r['sentiment']['basic_sentiment']['classification'] == 'Positive']) > len([r for r in results if r['sentiment']['basic_sentiment']['classification'] == 'Negative']) else 'negative_dominant'
            }
        }
    
    def _generate_action_items(self, results: List[Dict], alerts: Dict) -> List[str]:
        """Generate specific action items for analysts"""
        action_items = []
        
        if alerts['high_priority']:
            action_items.append(f"Address {len(alerts['high_priority'])} high-priority negative sentiment items immediately")
        
        if alerts['opportunities']:
            action_items.append(f"Leverage {len(alerts['opportunities'])} positive feedback opportunities for improvement")
        
        # Analyze aspects for action items
        aspect_issues = defaultdict(int)
        for result in results:
            for aspect, details in result['sentiment']['aspect_sentiment'].items():
                if details['sentiment'] == 'Negative':
                    aspect_issues[aspect] += 1
        
        for aspect, count in aspect_issues.items():
            if count > 1:
                action_items.append(f"Investigate and improve {aspect} (negative mentions: {count})")
        
        return action_items
    
    def _calculate_sentiment_health(self, summary: Dict) -> str:
        """Calculate overall sentiment health score"""
        if not summary:
            return "unknown"
        
        sentiment_counts = summary.get('sentiment_counts', {})
        total = sum(sentiment_counts.values())
        
        if total == 0:
            return "unknown"
        
        positive_ratio = sentiment_counts.get('Positive', 0) / total
        negative_ratio = sentiment_counts.get('Negative', 0) / total
        
        if positive_ratio > 0.6:
            return "excellent"
        elif positive_ratio > 0.4:
            return "good"
        elif negative_ratio > 0.4:
            return "concerning"
        else:
            return "neutral"
    
    def _identify_sentiment_patterns(self, results: List[Dict]) -> List[str]:
        """Identify patterns in sentiment data"""
        patterns = []
        
        # Analyze emotion patterns
        emotions = [r['sentiment']['emotions']['dominant_emotion'] for r in results]
        emotion_counter = Counter(emotions)
        
        if len(emotion_counter) > 0:
            most_common = emotion_counter.most_common(1)[0]
            if most_common[1] > len(results) * 0.4:
                patterns.append(f"Dominant emotion pattern: {most_common[0]} appears in {most_common[1]} texts")
        
        return patterns
    
    def _identify_emotional_drivers(self, results: List[Dict]) -> List[str]:
        """Identify what drives different emotions"""
        drivers = []
        
        # Analyze aspect-emotion relationships
        aspect_emotion_map = defaultdict(list)
        
        for result in results:
            dominant_emotion = result['sentiment']['emotions']['dominant_emotion']
            for aspect in result['sentiment']['aspect_sentiment'].keys():
                aspect_emotion_map[aspect].append(dominant_emotion)
        
        for aspect, emotions in aspect_emotion_map.items():
            emotion_counter = Counter(emotions)
            if emotion_counter:
                most_common = emotion_counter.most_common(1)[0]
                drivers.append(f"{aspect} primarily drives {most_common[0]} emotion")
        
        return drivers
    
    def _analyze_aspect_performance(self, results: List[Dict]) -> Dict:
        """Analyze performance of different aspects"""
        aspect_performance = {}
        
        all_aspects = set()
        for result in results:
            all_aspects.update(result['sentiment']['aspect_sentiment'].keys())
        
        for aspect in all_aspects:
            sentiments = []
            for result in results:
                if aspect in result['sentiment']['aspect_sentiment']:
                    sentiments.append(result['sentiment']['aspect_sentiment'][aspect]['sentiment'])
            
            if sentiments:
                sentiment_counter = Counter(sentiments)
                positive_ratio = sentiment_counter.get('Positive', 0) / len(sentiments)
                
                if positive_ratio > 0.6:
                    performance = "excellent"
                elif positive_ratio > 0.4:
                    performance = "good"
                elif sentiment_counter.get('Negative', 0) / len(sentiments) > 0.4:
                    performance = "poor"
                else:
                    performance = "neutral"
                
                aspect_performance[aspect] = {
                    'performance': performance,
                    'sentiment_distribution': dict(sentiment_counter),
                    'total_mentions': len(sentiments)
                }
        
        return aspect_performance
    
    def _empty_report(self) -> Dict:
        """Return empty report structure"""
        return {
            'summary': {},
            'sentiment_distribution': {},
            'emotion_analysis': {},
            'aspect_insights': {},
            'language_distribution': {},
            'quality_metrics': {},
            'key_insights': [],
            'recommendations': [],
            'individual_results': [],
            'generated_at': datetime.now().isoformat()
        }
