"""
Test script to debug NLP modules
"""

import sys
sys.path.append('src')

from sentiment_analyzer import SentimentAnalyzer
from aspect_detector import AspectDetector
from cuisine_classifier import CuisineClassifier
from entity_recognition import EntityRecognizer

# Test review
test_review = """
Amazing Indian cuisine! The butter chicken and garlic naan were outstanding. 
Rich, flavorful curry with just the right amount of spice. Quick and efficient service. 
The place has a cozy, traditional ambiance with beautiful decor. 
Great value for money at $25 per person including appetizers and dessert.
"""

print("="*60)
print("TESTING NLP MODULES")
print("="*60)

print("\n1. SENTIMENT ANALYSIS")
print("-"*60)
sentiment_analyzer = SentimentAnalyzer()
result = sentiment_analyzer.analyze(test_review)
print(f"Sentiment: {result['sentiment']}")
print(f"Confidence: {result['confidence']}")

print("\n2. CUISINE CLASSIFICATION")
print("-"*60)
cuisine_classifier = CuisineClassifier()
result = cuisine_classifier.classify(test_review)
print(f"Cuisine: {result['cuisine']}")
print(f"Confidence: {result['confidence']}")

print("\n3. ASPECT DETECTION")
print("-"*60)
aspect_detector = AspectDetector()
aspects = aspect_detector.get_summary(test_review)
for aspect, sentiment in aspects.items():
    print(f"{aspect}: {sentiment}")

print("\n4. ENTITY RECOGNITION")
print("-"*60)
entity_recognizer = EntityRecognizer()
entities = entity_recognizer.extract_entities(test_review)
for entity_type, entity_list in entities.items():
    if entity_list:
        print(f"{entity_type}: {', '.join(entity_list)}")

print("\n" + "="*60)
print("TEST COMPLETE")
print("="*60)
