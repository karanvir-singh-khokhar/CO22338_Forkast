"""
Test cuisine classification
"""

import sys
sys.path.append('src')

from cuisine_classifier import CuisineClassifier

classifier = CuisineClassifier()

test_reviews = [
    ("Incredible Korean BBQ spot! The galbi and bulgogi were marinated perfectly.", "Korean"),
    ("Amazing butter chicken and garlic naan!", "Indian"),
    ("Best sushi I've ever had.", "Japanese"),
    ("Love their tacos and guacamole.", "Mexican"),
    ("The pasta carbonara was delicious.", "Italian"),
    ("Tried Ethiopian food for the first time at Habesha Restaurant. The doro wat and injera bread were interesting.", "Ethiopian"),
]

print("="*60)
print("TESTING CUISINE CLASSIFICATION")
print("="*60)

for review, expected in test_reviews:
    result = classifier.classify(review)
    status = "✅" if result['cuisine'] == expected else "❌"
    print(f"\n{status} Review: {review[:50]}...")
    print(f"   Expected: {expected} | Got: {result['cuisine']} ({result['confidence']:.1%})")
