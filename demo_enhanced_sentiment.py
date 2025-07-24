#!/usr/bin/env python3
"""
Demonstration script for Enhanced Sentiment Analysis
Shows the improvements made to the NLP module and analysis capabilities
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent / 'src'))

from modules.nlp.sentiment import sentiment_analysis, sentiment_analysis_comprehensive
from modules.nlp.enhanced_sentiment import EnhancedSentimentAnalyzer, SentimentFilter
from modules.analysis.sentiment_analysis import SentimentAnalysisReport

def demonstrate_basic_improvements():
    """Demonstrate basic sentiment analysis improvements"""
    print("=" * 60)
    print("BASIC SENTIMENT ANALYSIS IMPROVEMENTS")
    print("=" * 60)
    
    texts = [
        "I love this amazing product! The quality is outstanding!",
        "This is terrible. Poor quality and awful service.",
        "The product is okay, nothing special.",
        "Absolutely fantastic! Best purchase I've made this year!"
    ]
    
    print("\n📊 Basic Sentiment Classification:")
    for i, text in enumerate(texts, 1):
        result = sentiment_analysis(text)
        print(f"{i}. '{text[:50]}...' → {result}")

def demonstrate_comprehensive_analysis():
    """Demonstrate comprehensive multi-dimensional analysis"""
    print("\n" + "=" * 60)
    print("COMPREHENSIVE MULTI-DIMENSIONAL ANALYSIS")
    print("=" * 60)
    
    text = "I absolutely love this product! The quality is amazing but the price is quite expensive. The service was fantastic and delivery was super fast!"
    
    print(f"\n📝 Analyzing: '{text}'\n")
    
    result = sentiment_analysis_comprehensive(text)
    
    print("🎯 Basic Sentiment:")
    print(f"   Classification: {result['basic_sentiment']['classification']}")
    print(f"   Polarity: {result['basic_sentiment']['polarity']:.3f}")
    print(f"   Confidence: {result['overall_confidence']:.3f}")
    
    print("\n😊 Emotion Analysis:")
    print(f"   Dominant Emotion: {result['emotions']['dominant_emotion']}")
    print(f"   Emotion Scores: {result['emotions']['scores']}")
    
    print(f"\n⚡ Intensity & Subjectivity:")
    print(f"   Intensity: {result['intensity']['intensity']:.3f}")
    print(f"   Subjectivity: {result['subjectivity']['classification']} ({result['subjectivity']['score']:.3f})")
    
    print(f"\n🏷️ Aspect-Based Sentiment:")
    for aspect, details in result['aspect_sentiment'].items():
        print(f"   {aspect.title()}: {details['sentiment']} (polarity: {details['polarity']:.3f})")
    
    print(f"\n🌍 Language: {result['language']}")

def demonstrate_filtering_capabilities():
    """Demonstrate filtering and classification capabilities"""
    print("\n" + "=" * 60)
    print("FILTERING AND CLASSIFICATION CAPABILITIES")
    print("=" * 60)
    
    analyzer = EnhancedSentimentAnalyzer()
    sentiment_filter = SentimentFilter()
    
    # Analyze multiple texts
    texts = [
        "This product is amazing! I love it!",
        "Terrible quality, very disappointed",
        "The service is excellent but price is too high",
        "Average product, nothing special",
        "Fantastic experience! Highly recommended!",
        "Poor customer support, very frustrated"
    ]
    
    print("\n🔍 Analyzing multiple texts...")
    results = []
    for text in texts:
        result = analyzer.analyze_comprehensive(text)
        results.append(result)
        
    print(f"📊 Total texts analyzed: {len(results)}")
    
    # Demonstrate filtering
    positive_results = sentiment_filter.filter_by_sentiment(results, 'Positive')
    high_confidence_results = sentiment_filter.filter_by_confidence(results, 0.7)
    high_intensity_results = sentiment_filter.filter_by_intensity(results, 0.5)
    
    print(f"\n📈 Filtering Results:")
    print(f"   Positive sentiments: {len(positive_results)}")
    print(f"   High confidence (>0.7): {len(high_confidence_results)}")
    print(f"   High intensity (>0.5): {len(high_intensity_results)}")

def demonstrate_analyst_context():
    """Demonstrate enriched analyst context and reporting"""
    print("\n" + "=" * 60)
    print("ENRICHED ANALYST CONTEXT AND REPORTING")
    print("=" * 60)
    
    report_generator = SentimentAnalysisReport()
    
    # Sample customer feedback texts
    feedback_texts = [
        "I love this product! The quality is excellent and delivery was fast!",
        "Terrible experience. The product broke after one day and customer service is awful.",
        "Good product overall, but the price is a bit high for what you get.",
        "Amazing quality! Best purchase I've made. Highly recommend!",
        "The product is okay, nothing special. Average quality and service.",
        "Poor packaging and slow delivery. Product quality is mediocre.",
        "Excellent customer support! They helped me solve my issue quickly.",
        "Disappointed with the product quality. Expected much better for the price."
    ]
    
    print(f"\n📋 Generating comprehensive analysis report for {len(feedback_texts)} feedback items...")
    
    # Generate comprehensive report
    report = report_generator.analyze_text_collection(feedback_texts)
    
    print("\n📊 SUMMARY STATISTICS:")
    summary = report['summary']
    print(f"   Total texts: {summary['total_texts']}")
    print(f"   Sentiment distribution: {dict(summary['sentiment_counts'])}")
    print(f"   Average confidence: {summary['average_confidence']:.3f}")
    print(f"   Average intensity: {summary['average_intensity']:.3f}")
    
    print("\n🔍 KEY INSIGHTS:")
    for insight in report['key_insights'][:3]:
        print(f"   • {insight}")
    
    print("\n💡 RECOMMENDATIONS:")
    for rec in report['recommendations'][:3]:
        print(f"   • {rec}")
    
    # Generate analyst context
    print("\n📈 ANALYST CONTEXT:")
    context = report_generator.generate_analyst_context(report)
    analyst_summary = context['analyst_summary']
    
    print(f"   Sentiment Health: {analyst_summary['overall_sentiment_health']}")
    print(f"   High Priority Issues: {len(analyst_summary['key_concerns'])}")
    print(f"   Positive Opportunities: {len(analyst_summary['opportunities'])}")
    
    print("\n⚠️ PRIORITY ALERTS:")
    for alert in context['priority_alerts']['high_priority'][:2]:
        print(f"   • {alert['reason']}: '{alert['text']}'")
    
    print("\n✅ ACTION ITEMS:")
    for item in context['action_items'][:3]:
        print(f"   • {item}")

def demonstrate_multilingual_support():
    """Demonstrate multilingual sentiment analysis"""
    print("\n" + "=" * 60)
    print("MULTILINGUAL SENTIMENT ANALYSIS")
    print("=" * 60)
    
    analyzer = EnhancedSentimentAnalyzer()
    
    multilingual_texts = [
        ("English", "This product is absolutely fantastic! I love it!"),
        ("Portuguese", "Este produto é incrível! Eu amo muito!"),
        ("English", "Terrible quality and poor service"),
        ("Portuguese", "Qualidade terrível e atendimento ruim"),
    ]
    
    print("\n🌍 Analyzing texts in different languages:")
    
    for language, text in multilingual_texts:
        result = analyzer.analyze_comprehensive(text)
        print(f"\n{language}: '{text}'")
        print(f"   Detected Language: {result['language']}")
        print(f"   Sentiment: {result['basic_sentiment']['classification']}")
        print(f"   Confidence: {result['overall_confidence']:.3f}")

def main():
    """Main demonstration function"""
    print("🚀 SIBILA - ENHANCED SENTIMENT ANALYSIS DEMONSTRATION")
    print("Showcasing improvements to NLP module and analyst context enrichment")
    
    try:
        demonstrate_basic_improvements()
        demonstrate_comprehensive_analysis()
        demonstrate_filtering_capabilities()
        demonstrate_analyst_context()
        demonstrate_multilingual_support()
        
        print("\n" + "=" * 60)
        print("✅ DEMONSTRATION COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("\n🎯 Key Improvements Implemented:")
        print("   • Multi-dimensional sentiment analysis (emotion, intensity, subjectivity)")
        print("   • Aspect-based sentiment analysis")
        print("   • Enhanced filtering and classification capabilities")
        print("   • Comprehensive analyst context and reporting")
        print("   • Multilingual support (Portuguese/English)")
        print("   • Extensible architecture for different analysis types")
        print("   • Improved precision with confidence scoring")
        print("   • Integration with existing NLP modules")
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()