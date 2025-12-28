"""
Sentiment Analysis Module
Analyzes the overall sentiment of restaurant reviews
"""

from textblob import TextBlob
from typing import Dict, Tuple
import pandas as pd

# Try to import transformers, but make it optional
try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("⚠️  transformers library not installed. Using TextBlob for sentiment analysis.")


class SentimentAnalyzer:
    """
    Sentiment analysis using multiple approaches:
    1. TextBlob (simple, rule-based)
    2. Transformers (deep learning, more accurate)
    """
    
    def __init__(self, method='textblob'):
        """
        Initialize sentiment analyzer
        
        Args:
            method: 'textblob' or 'transformer'
        """
        self.method = method
        
        if method == 'transformer':
            if not TRANSFORMERS_AVAILABLE:
                print("⚠️  Transformers not available. Falling back to TextBlob.")
                self.method = 'textblob'
            else:
                print("Loading transformer model... (this may take a moment)")
                self.model = pipeline(
                    "sentiment-analysis",
                    model="distilbert-base-uncased-finetuned-sst-2-english"
                )
                print("✅ Model loaded successfully!")
    
    def analyze_textblob(self, text: str) -> Tuple[str, float]:
        """
        Analyze sentiment using TextBlob
        
        Args:
            text: Review text
            
        Returns:
            Tuple of (sentiment_label, polarity_score)
        """
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        # More nuanced sentiment classification
        if polarity > 0.3:
            sentiment = 'positive'
        elif polarity < -0.3:
            sentiment = 'negative'
        elif polarity > 0.05:
            sentiment = 'slightly positive'
        elif polarity < -0.05:
            sentiment = 'slightly negative'
        else:
            sentiment = 'neutral'
        
        # Normalize score to 0-1 range
        score = abs(polarity)
        
        # Simplify for display
        if 'slightly' in sentiment:
            sentiment = 'neutral'
            
        return sentiment, score
    
    def analyze_transformer(self, text: str) -> Tuple[str, float]:
        """
        Analyze sentiment using transformer model
        
        Args:
            text: Review text
            
        Returns:
            Tuple of (sentiment_label, confidence_score)
        """
        # Truncate text if too long (BERT limit is 512 tokens)
        max_length = 512
        if len(text.split()) > max_length:
            text = ' '.join(text.split()[:max_length])
        
        result = self.model(text)[0]
        sentiment = result['label'].lower()  # POSITIVE or NEGATIVE
        score = result['score']
        
        return sentiment, score
    
    def analyze(self, text: str) -> Dict[str, any]:
        """
        Main analysis method
        
        Args:
            text: Review text
            
        Returns:
            Dictionary with sentiment, score, and details
        """
        if self.method == 'textblob':
            sentiment, score = self.analyze_textblob(text)
        else:
            sentiment, score = self.analyze_transformer(text)
        
        return {
            'sentiment': sentiment,
            'confidence': round(score, 4),
            'method': self.method
        }
    
    def batch_analyze(self, texts: list) -> pd.DataFrame:
        """
        Analyze multiple reviews
        
        Args:
            texts: List of review texts
            
        Returns:
            DataFrame with results
        """
        results = []
        for text in texts:
            result = self.analyze(text)
            results.append(result)
        
        return pd.DataFrame(results)


def get_sentiment_emoji(sentiment: str) -> str:
    """Return emoji for sentiment"""
    emoji_map = {
        'positive': '😊',
        'negative': '😞',
        'neutral': '😐'
    }
    return emoji_map.get(sentiment, '❓')


# Quick test function
if __name__ == "__main__":
    # Test the sentiment analyzer
    analyzer = SentimentAnalyzer(method='textblob')
    
    test_reviews = [
        "The food was absolutely amazing! Best restaurant ever.",
        "Terrible service and cold food. Very disappointed.",
        "It was okay, nothing special but not bad either."
    ]
    
    print("Testing Sentiment Analyzer\n" + "="*50)
    for review in test_reviews:
        result = analyzer.analyze(review)
        emoji = get_sentiment_emoji(result['sentiment'])
        print(f"\nReview: {review}")
        print(f"Sentiment: {result['sentiment']} {emoji}")
        print(f"Confidence: {result['confidence']:.2%}")
