"""
Test improved NLP accuracy
"""

import sys
sys.path.append('src')

from sentiment_analyzer import SentimentAnalyzer
from aspect_detector import AspectDetector

# Test reviews with clear sentiments
test_reviews = [
    {
        "text": "The food was terrible and the service was horrible. Never coming back!",
        "expected_sentiment": "negative",
        "expected_food": "negative",
        "expected_service": "negative"
    },
    {
        "text": "Amazing food! However, the service was extremely slow and rude.",
        "expected_sentiment": "positive",
        "expected_food": "positive",
        "expected_service": "negative"
    },
    {
        "text": "The pasta was delicious but overpriced. Service was okay.",
        "expected_sentiment": "neutral",
        "expected_food": "positive",
        "expected_service": "neutral"
    }
]

print("="*70)
print("TESTING IMPROVED NLP ACCURACY")
print("="*70)

sentiment_analyzer = SentimentAnalyzer()
aspect_detector = AspectDetector()

for i, test in enumerate(test_reviews, 1):
    print(f"\n--- Test {i} ---")
    print(f"Review: {test['text']}")
    
    # Sentiment
    sentiment_result = sentiment_analyzer.analyze(test['text'])
    sentiment_match = "✅" if sentiment_result['sentiment'] == test['expected_sentiment'] else "⚠️"
    print(f"{sentiment_match} Sentiment: {sentiment_result['sentiment']} (expected: {test['expected_sentiment']})")
    
    # Aspects
    aspects = aspect_detector.get_summary(test['text'])
    
    if 'food' in aspects:
        food_match = "✅" if aspects['food'] == test['expected_food'] else "⚠️"
        print(f"{food_match} Food: {aspects['food']} (expected: {test['expected_food']})")
    
    if 'service' in aspects:
        service_match = "✅" if aspects['service'] == test['expected_service'] else "⚠️"
        print(f"{service_match} Service: {aspects['service']} (expected: {test['expected_service']})")

print("\n" + "="*70)
