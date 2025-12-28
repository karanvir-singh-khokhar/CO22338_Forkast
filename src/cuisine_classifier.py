"""
Cuisine Classification Module
Classifies reviews into cuisine types based on text content
"""

from typing import Dict, List, Tuple
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle


class CuisineClassifier:
    """
    Classifies restaurant reviews by cuisine type using keyword matching
    and machine learning
    """
    
    def __init__(self):
        """Initialize with cuisine keywords"""
        
        self.cuisine_keywords = {
            'Italian': [
                'pasta', 'pizza', 'spaghetti', 'lasagna', 'risotto', 'gelato',
                'tiramisu', 'parmigiana', 'carbonara', 'bruschetta', 'gnocchi',
                'italian', 'marinara', 'alfredo', 'mozzarella', 'parmesan',
                'fettuccine', 'ravioli'
            ],
            'Chinese': [
                'noodle', 'dumpling', 'wonton', 'fried rice', 'chow mein',
                'kung pao', 'sweet and sour', 'dim sum', 'chinese', 'szechuan',
                'cantonese', 'spring roll', 'fortune cookie', 'stir fry', 'soy sauce',
                'peking duck', 'hot pot'
            ],
            'Indian': [
                'curry', 'naan', 'biryani', 'tandoori', 'masala', 'samosa',
                'paneer', 'tikka', 'korma', 'vindaloo', 'dal', 'indian',
                'chapati', 'butter chicken', 'roti', 'chai', 'dosa', 'idli'
            ],
            'Mexican': [
                'taco', 'burrito', 'quesadilla', 'enchilada', 'guacamole',
                'salsa', 'nachos', 'fajita', 'chimichanga', 'mexican',
                'tortilla', 'jalapeño', 'margarita', 'cilantro', 'tamale'
            ],
            'Japanese': [
                'sushi', 'sashimi', 'ramen', 'tempura', 'teriyaki', 'miso',
                'wasabi', 'sake', 'udon', 'japanese', 'hibachi', 'edamame',
                'bento', 'katsu', 'soba', 'california roll', 'tonkatsu'
            ],
            'Korean': [
                'korean', 'bbq', 'galbi', 'bulgogi', 'kimchi', 'bibimbap',
                'korean bbq', 'gochujang', 'banchan', 'soju', 'kbbq',
                'korean fried chicken', 'japchae', 'tteokbokki'
            ],
            'American': [
                'burger', 'fries', 'steak', 'ribs', 'sandwich',
                'hot dog', 'mac and cheese', 'fried chicken', 'american',
                'coleslaw', 'milkshake', 'diner', 'breakfast', 'bacon', 'eggs',
                'wings', 'pulled pork'
            ],
            'Thai': [
                'pad thai', 'tom yum', 'thai', 'coconut', 'lemongrass',
                'basil', 'peanut sauce', 'mango', 'sticky rice',
                'green curry', 'red curry', 'papaya salad'
            ],
            'Mediterranean': [
                'hummus', 'falafel', 'kebab', 'gyro', 'shawarma', 'pita',
                'mediterranean', 'greek', 'olive', 'feta', 'tzatziki', 'lamb',
                'baba ganoush', 'tabbouleh'
            ],
            'Ethiopian': [
                'ethiopian', 'injera', 'doro wat', 'berbere', 'kitfo',
                'habesha', 'teff', 'mesob'
            ],
            'Brazilian': [
                'brazilian', 'picanha', 'fogo', 'churrasco', 'pao de queijo',
                'caipirinha', 'feijoada', 'brigadeiro'
            ],
            'Vietnamese': [
                'pho', 'banh mi', 'vietnamese', 'spring rolls', 'bun',
                'vermicelli', 'fish sauce', 'lemongrass'
            ],
            'French': [
                'french', 'foie gras', 'escargot', 'croissant', 'crepe',
                'ratatouille', 'coq au vin', 'bouillabaisse', 'beef wellington'
            ]
        }
        
        self.model = None
        self.vectorizer = None
    
    def classify_by_keywords(self, text: str) -> Tuple[str, float]:
        """
        Classify cuisine using keyword matching
        
        Args:
            text: Review text
            
        Returns:
            Tuple of (cuisine_type, confidence_score)
        """
        text_lower = text.lower()
        
        # Check for explicit cuisine mentions first (highest priority)
        explicit_mentions = {
            'korean': 'Korean',
            'korean bbq': 'Korean',
            'kbbq': 'Korean',
            'indian': 'Indian',
            'italian': 'Italian',
            'chinese': 'Chinese',
            'japanese': 'Japanese',
            'mexican': 'Mexican',
            'thai': 'Thai',
            'ethiopian': 'Ethiopian',
            'brazilian': 'Brazilian',
            'vietnamese': 'Vietnamese',
            'french': 'French',
            'mediterranean': 'Mediterranean',
            'american': 'American'
        }
        
        for mention, cuisine in explicit_mentions.items():
            if mention in text_lower:
                return cuisine, 1.0
        
        # Count keyword matches for each cuisine with weighted scoring
        scores = {}
        for cuisine, keywords in self.cuisine_keywords.items():
            weighted_score = 0
            for keyword in keywords:
                if keyword in text_lower:
                    # Give higher weight to longer, more specific keywords
                    weight = len(keyword.split())
                    weighted_score += weight
            scores[cuisine] = weighted_score
        
        # Get cuisine with highest score
        if max(scores.values()) == 0:
            return 'Unknown', 0.0
        
        best_cuisine = max(scores, key=scores.get)
        
        # Calculate confidence (normalized score)
        total_matches = sum(scores.values())
        confidence = scores[best_cuisine] / total_matches if total_matches > 0 else 0
        
        return best_cuisine, confidence
        if max(scores.values()) == 0:
            return 'Unknown', 0.0
        
        best_cuisine = max(scores, key=scores.get)
        
        # Calculate confidence (normalized score)
        total_matches = sum(scores.values())
        confidence = scores[best_cuisine] / total_matches if total_matches > 0 else 0
        
        return best_cuisine, confidence
    
    def classify(self, text: str) -> Dict[str, any]:
        """
        Main classification method
        
        Args:
            text: Review text
            
        Returns:
            Dictionary with cuisine type and confidence
        """
        cuisine, confidence = self.classify_by_keywords(text)
        
        return {
            'cuisine': cuisine,
            'confidence': round(confidence, 4),
            'method': 'keyword_matching'
        }
    
    def get_all_scores(self, text: str) -> Dict[str, int]:
        """
        Get match scores for all cuisines
        
        Args:
            text: Review text
            
        Returns:
            Dictionary mapping cuisines to match counts
        """
        text_lower = text.lower()
        scores = {}
        
        for cuisine, keywords in self.cuisine_keywords.items():
            count = sum(1 for keyword in keywords if keyword in text_lower)
            if count > 0:
                scores[cuisine] = count
        
        # Sort by score
        return dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))


def get_cuisine_emoji(cuisine: str) -> str:
    """Return emoji for cuisine type"""
    emoji_map = {
        'Italian': '🍝',
        'Chinese': '🥡',
        'Indian': '🍛',
        'Mexican': '🌮',
        'Japanese': '🍣',
        'Korean': '🍖',
        'American': '🍔',
        'Thai': '🍜',
        'Mediterranean': '🥙',
        'Ethiopian': '🍲',
        'Brazilian': '🥩',
        'Vietnamese': '🥢',
        'French': '🥖',
        'Unknown': '🍽️'
    }
    return emoji_map.get(cuisine, '🍽️')


# Test function
if __name__ == "__main__":
    classifier = CuisineClassifier()
    
    test_reviews = [
        "Amazing butter chicken and naan! The curry was perfect.",
        "Best sushi I've ever had. Fresh sashimi and great miso soup.",
        "Love their tacos and guacamole. Authentic Mexican food!",
        "The pasta carbonara was delicious. Great Italian restaurant.",
        "Excellent pad thai and tom yum soup. Very authentic Thai food."
    ]
    
    print("Testing Cuisine Classifier\n" + "="*50)
    for review in test_reviews:
        result = classifier.classify(review)
        emoji = get_cuisine_emoji(result['cuisine'])
        print(f"\nReview: {review}")
        print(f"Cuisine: {result['cuisine']} {emoji}")
        print(f"Confidence: {result['confidence']:.2%}")
