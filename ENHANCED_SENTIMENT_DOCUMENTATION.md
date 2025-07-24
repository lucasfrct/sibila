# Enhanced Sentiment Analysis Documentation

## Overview

The Sibila NLP module has been significantly enhanced with comprehensive sentiment analysis capabilities that provide multi-dimensional analysis and enriched context for analysts. The improvements address the original request for better sentiment analysis precision and diverse analysis dimensions.

## Key Features

### 1. Multi-Dimensional Sentiment Analysis

- **Basic Sentiment**: Enhanced classification (Positive/Negative/Neutral) using combined TextBlob + VADER analysis
- **Emotion Detection**: Identifies 6 emotions (joy, anger, fear, sadness, surprise, disgust) in Portuguese and English
- **Intensity Scoring**: Measures sentiment strength and confidence levels
- **Subjectivity Analysis**: Classifies text as Objective, Subjective, or Highly Subjective
- **Aspect-Based Analysis**: Analyzes sentiment for specific aspects (quality, price, service, delivery, product)
- **Language Detection**: Supports Portuguese and English with automatic detection

### 2. Enhanced Classification & Filtering

- Filter by sentiment type, confidence level, emotion, intensity, and subjectivity
- Classify results into priority levels (high/medium/low priority, positive feedback)
- Extensible filter architecture for custom criteria

### 3. Enriched Analyst Context

- Comprehensive analysis reports with summary statistics
- Priority alerts and opportunity identification
- Actionable recommendations and specific action items
- Sentiment health scoring and quality metrics

## Usage Examples

### Basic Sentiment Analysis (Backward Compatible)

```python
from modules.nlp.sentiment import sentiment_analysis

# Simple sentiment classification
result = sentiment_analysis("I love this product!")
print(result)  # Output: "Positive"
```

### Comprehensive Multi-Dimensional Analysis

```python
from modules.nlp.sentiment import sentiment_analysis_comprehensive

# Detailed analysis with multiple dimensions
result = sentiment_analysis_comprehensive("I love this product! The quality is excellent but the price is expensive.")

print(f"Sentiment: {result['basic_sentiment']['classification']}")
print(f"Dominant Emotion: {result['emotions']['dominant_emotion']}")
print(f"Language: {result['language']}")
print(f"Aspects: {list(result['aspect_sentiment'].keys())}")
print(f"Confidence: {result['overall_confidence']:.3f}")
```

### Comprehensive Analysis Report for Multiple Texts

```python
from modules.analysis.sentiment_analysis import SentimentAnalysisReport

# Create report generator
report_generator = SentimentAnalysisReport()

# Analyze multiple texts
texts = [
    "I love this product! Great quality!",
    "Terrible service and poor quality.",
    "Average product, nothing special."
]

# Generate comprehensive report
report = report_generator.analyze_text_collection(texts)

# Access summary statistics
print(f"Total texts: {report['summary']['total_texts']}")
print(f"Sentiment distribution: {dict(report['summary']['sentiment_counts'])}")
print(f"Key insights: {report['key_insights']}")
print(f"Recommendations: {report['recommendations']}")

# Generate enriched analyst context
context = report_generator.generate_analyst_context(report)
print(f"Sentiment health: {context['analyst_summary']['overall_sentiment_health']}")
print(f"Action items: {context['action_items']}")
```

### Filtering and Classification

```python
from modules.nlp.enhanced_sentiment import EnhancedSentimentAnalyzer, SentimentFilter

analyzer = EnhancedSentimentAnalyzer()
sentiment_filter = SentimentFilter()

# Analyze texts
results = []
for text in texts:
    result = analyzer.analyze_comprehensive(text)
    results.append(result)

# Filter by criteria
positive_results = sentiment_filter.filter_by_sentiment(results, 'Positive')
high_confidence = sentiment_filter.filter_by_confidence(results, 0.7)
high_intensity = sentiment_filter.filter_by_intensity(results, 0.5)
```

## API Reference

### Enhanced Sentiment Analyzer

#### `EnhancedSentimentAnalyzer.analyze_comprehensive(text: str) -> Dict`

Performs comprehensive sentiment analysis with multiple dimensions.

**Returns:**
```python
{
    'text': str,
    'language': str,  # 'portuguese', 'english', or 'unknown'
    'basic_sentiment': {
        'classification': str,  # 'Positive', 'Negative', 'Neutral'
        'polarity': float,  # -1.0 to 1.0
        'confidence': float  # 0.0 to 1.0
    },
    'emotions': {
        'scores': dict,  # emotion -> score mapping
        'dominant_emotion': str,  # primary emotion detected
        'dominant_score': float
    },
    'intensity': {
        'intensity': float,  # 0.0 to 1.0
        'confidence': float  # 0.0 to 1.0
    },
    'subjectivity': {
        'score': float,  # 0.0 to 1.0
        'classification': str  # 'Objective', 'Subjective', 'Highly Subjective'
    },
    'aspect_sentiment': {
        # aspect_name -> sentiment details
    },
    'overall_confidence': float  # 0.0 to 1.0
}
```

### Sentiment Filter

#### Available Filter Methods:
- `filter_by_sentiment(results, sentiment_type)`: Filter by 'Positive', 'Negative', 'Neutral'
- `filter_by_emotion(results, emotion)`: Filter by dominant emotion
- `filter_by_confidence(results, min_confidence)`: Filter by minimum confidence score
- `filter_by_intensity(results, min_intensity)`: Filter by minimum intensity
- `filter_by_subjectivity(results, subjectivity_type)`: Filter by subjectivity level
- `filter_by_aspect(results, aspect)`: Filter by aspect presence

### Analysis Report Generator

#### `SentimentAnalysisReport.analyze_text_collection(texts: List[str]) -> Dict`

Generates comprehensive analysis report for multiple texts.

#### `SentimentAnalysisReport.generate_analyst_context(report: Dict) -> Dict`

Creates enriched analyst context with priority alerts, trends, and action items.

## Installation Requirements

The enhanced sentiment analysis requires the following dependencies (automatically added to requirements.txt):

```
textblob==0.17.1
vaderSentiment==3.3.2
```

## Testing

Run the comprehensive test suite:

```bash
python -m pytest tests/test_enhanced_sentiment.py -v
```

Run the demonstration script:

```bash
python demo_enhanced_sentiment.py
```

## Key Improvements

1. **Enhanced Precision**: Combined TextBlob + VADER analysis for better accuracy
2. **Diverse Analysis Dimensions**: 6 different analysis dimensions (sentiment, emotion, intensity, subjectivity, aspects, language)
3. **Analyst Context Enrichment**: Comprehensive reporting with actionable insights
4. **Extensible Architecture**: Easy to add new analysis dimensions and filters
5. **Multilingual Support**: Portuguese and English language support
6. **Backward Compatibility**: Existing code continues to work unchanged
7. **Quality Assurance**: Comprehensive test coverage and error handling

## Integration with Existing Modules

The enhanced sentiment analysis integrates seamlessly with existing Sibila modules:

- **NLP Module**: Extends existing sentiment analysis capabilities
- **Analysis Module**: Provides enriched context for analysts
- **Classifier Module**: Can be used together for advanced text classification
- **Feature Extractor**: Compatible for enhanced text analysis workflows

This implementation successfully addresses the original requirements for improved sentiment analysis precision and diverse analysis dimensions while providing significant value to analysts through enriched context and actionable insights.