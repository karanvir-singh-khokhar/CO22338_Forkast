"""
Aspect-Based Sentiment Analysis
Extracts opinions about specific aspects: food, service, ambiance, price
"""

import re
from typing import Dict, List
import spacy
from textblob import TextBlob


class AspectDetector:
    """
    Detects and analyzes sentiment for specific aspects of restaurant reviews
    """
    
    def __init__(self):
        """Initialize aspect detector with keyword dictionaries"""
        
        # Define aspect keywords (expanded and improved)
        self.aspect_keywords = {
            'food': [
                'food', 'dish', 'meal', 'taste', 'flavor', 'flavour', 'delicious', 'tasty',
                'menu', 'cuisine', 'recipe', 'ingredient', 'fresh', 'quality',
                'burger', 'pizza', 'pasta', 'salad', 'dessert', 'appetizer',
                'entree', 'chicken', 'beef', 'fish', 'vegetable', 'spicy', 'sweet',
                'bland', 'flavorless', 'stale', 'cold', 'overcooked', 'undercooked',
                'juicy', 'tender', 'crispy', 'soggy', 'burnt', 'raw'
            ],
            'service': [
                'service', 'staff', 'waiter', 'waitress', 'server', 'manager',
                'friendly', 'rude', 'attentive', 'slow', 'fast', 'professional',
                'helpful', 'employee', 'personnel', 'team', 'wait', 'serve',
                'ignored', 'forgot', 'efficient', 'courteous', 'polite', 'impolite'
            ],
            'ambiance': [
                'ambiance', 'atmosphere', 'decor', 'environment', 'vibe', 'mood',
                'cozy', 'romantic', 'loud', 'quiet', 'clean', 'dirty', 'lighting',
                'music', 'seating', 'interior', 'decoration', 'place', 'setting',
                'spacious', 'cramped', 'elegant', 'tacky', 'modern', 'outdated'
            ],
            'price': [
                'price', 'expensive', 'cheap', 'affordable', 'value', 'cost',
                'worth', 'overpriced', 'reasonable', 'budget', 'money', 'bill',
                'pricey', 'inexpensive', 'deal', 'discount', 'waste'
            ]
        }
        
        # Try to load spaCy model
        try:
            self.nlp = spacy.load('en_core_web_sm')
        except:
            print("⚠️  spaCy model not found. Install with: python -m spacy download en_core_web_sm")
            self.nlp = None
    
    def extract_aspect_sentences(self, text: str) -> Dict[str, List[str]]:
        """
        Extract sentences mentioning each aspect
        
        Args:
            text: Review text
            
        Returns:
            Dictionary mapping aspects to relevant sentences
        """
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip().lower() for s in sentences if s.strip()]
        
        aspect_sentences = {aspect: [] for aspect in self.aspect_keywords}
        
        for sentence in sentences:
            for aspect, keywords in self.aspect_keywords.items():
                if any(keyword in sentence for keyword in keywords):
                    aspect_sentences[aspect].append(sentence)
        
        return aspect_sentences
    
    def analyze_aspect_sentiment(self, sentences: List[str]) -> str:
        """
        Determine overall sentiment for an aspect based on its sentences
        
        Args:
            sentences: List of sentences about the aspect
            
        Returns:
            Sentiment: positive, negative, or neutral
        """
        if not sentences:
            return 'not mentioned'
        
        # Negative indicators for better detection
        negative_words = [
            'not', 'no', 'never', 'terrible', 'horrible', 'awful', 'bad', 'worst',
            'disappointing', 'poor', 'rude', 'slow', 'cold', 'stale', 'bland',
            'overpriced', 'expensive', 'waste', 'dirty', 'loud', 'cramped'
        ]
        
        # Positive indicators
        positive_words = [
            'great', 'excellent', 'amazing', 'fantastic', 'wonderful', 'perfect',
            'delicious', 'best', 'love', 'loved', 'good', 'nice', 'fresh',
            'friendly', 'attentive', 'cozy', 'beautiful', 'worth'
        ]
        
        polarities = []
        for sentence in sentences:
            sentence_lower = sentence.lower()
            
            # Check for negative words
            has_negative = any(word in sentence_lower for word in negative_words)
            has_positive = any(word in sentence_lower for word in positive_words)
            
            # Calculate polarity with word-based adjustment
            blob = TextBlob(sentence)
            polarity = blob.sentiment.polarity
            
            # Boost detection based on keywords
            if has_negative and polarity > -0.3:
                polarity = -0.5
            if has_positive and polarity < 0.3:
                polarity = 0.5
                
            polarities.append(polarity)
        
        avg_polarity = sum(polarities) / len(polarities)
        
        # More sensitive thresholds
        if avg_polarity > 0.15:
            return 'positive'
        elif avg_polarity < -0.15:
            return 'negative'
        else:
            return 'neutral'
    
    def extract_aspects(self, text: str) -> Dict[str, Dict]:
        """
        Main method to extract aspects and their sentiments
        
        Args:
            text: Review text
            
        Returns:
            Dictionary with aspect analysis
        """
        # Get sentences for each aspect
        aspect_sentences = self.extract_aspect_sentences(text)
        
        # Analyze sentiment for each aspect
        results = {}
        for aspect, sentences in aspect_sentences.items():
            sentiment = self.analyze_aspect_sentiment(sentences)
            results[aspect] = {
                'sentiment': sentiment,
                'sentences': sentences,
                'mentioned': len(sentences) > 0
            }
        
        return results
    
    def get_summary(self, text: str) -> Dict[str, str]:
        """
        Get simplified aspect-sentiment mapping
        
        Args:
            text: Review text
            
        Returns:
            Dictionary mapping aspects to sentiments
        """
        aspects = self.extract_aspects(text)
        return {
            aspect: data['sentiment'] 
            for aspect, data in aspects.items()
            if data['mentioned']
        }


def get_aspect_emoji(sentiment: str) -> str:
    """Return emoji for aspect sentiment"""
    emoji_map = {
        'positive': '✅',
        'negative': '❌',
        'neutral': '➖',
        'not mentioned': '⚪'
    }
    return emoji_map.get(sentiment, '❓')


# Test function
if __name__ == "__main__":
    detector = AspectDetector()
    
    test_review = """
    The food was absolutely delicious and fresh! The pasta was perfect.
    However, the service was extremely slow and the staff seemed uninterested.
    The ambiance was nice and cozy, perfect for a date night.
    A bit expensive but the quality of food made it worth it.
    """
    
    print("Testing Aspect Detector\n" + "="*50)
    print(f"Review: {test_review.strip()}\n")
    
    aspects = detector.get_summary(test_review)
    print("Aspect Analysis:")
    for aspect, sentiment in aspects.items():
        emoji = get_aspect_emoji(sentiment)
        print(f"  {emoji} {aspect.title()}: {sentiment}")
