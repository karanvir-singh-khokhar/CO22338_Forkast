"""
Named Entity Recognition Module
Extracts entities like dish names, restaurant names, and food items
"""

import spacy
from typing import Dict, List, Set
import re


class EntityRecognizer:
    """
    Extract named entities from restaurant reviews
    """
    
    def __init__(self):
        """Initialize NER with spaCy"""
        try:
            self.nlp = spacy.load('en_core_web_sm')
            self.spacy_available = True
        except:
            print("⚠️  spaCy model not found. Install with: python -m spacy download en_core_web_sm")
            self.spacy_available = False
        
        # Common dish patterns for fallback
        self.dish_patterns = [
            r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',  # e.g., Butter Chicken
            r'\b[A-Z][a-z]+ [a-z]+ [A-Z][a-z]+\b'  # e.g., Pad Thai Special
        ]
    
    def extract_with_spacy(self, text: str) -> Dict[str, List[str]]:
        """
        Extract entities using spaCy NER
        
        Args:
            text: Review text
            
        Returns:
            Dictionary with entity types and values
        """
        if not self.spacy_available:
            return self.extract_with_rules(text)
        
        doc = self.nlp(text)
        
        entities = {
            'dishes': [],
            'restaurants': [],
            'locations': [],
            'people': []
        }
        
        # Known food words to filter out false person detections
        food_indicators = ['naan', 'chicken', 'curry', 'biryani', 'tikka', 'paneer', 
                          'pizza', 'pasta', 'burger', 'sushi', 'taco', 'rice', 'bread',
                          'salad', 'soup', 'fish', 'beef', 'pork', 'lamb']
        
        # Words that are NOT people names
        false_names = ['rich', 'fresh', 'hot', 'cold', 'sweet', 'spicy', 'mild', 'tender']
        
        for ent in doc.ents:
            ent_lower = ent.text.lower()
            
            # Check if "person" entity is actually a food item or false positive
            if ent.label_ == 'PERSON':
                is_food = any(food in ent_lower for food in food_indicators)
                is_false_name = ent_lower in false_names
                
                if is_food:
                    entities['dishes'].append(ent.text)
                elif not is_false_name and len(ent.text) > 2:
                    entities['people'].append(ent.text)
            elif ent.label_ == 'ORG':
                entities['restaurants'].append(ent.text)
            elif ent.label_ == 'GPE':
                entities['locations'].append(ent.text)
            elif ent.label_ in ['PRODUCT', 'FOOD']:
                entities['dishes'].append(ent.text)
        
        # Remove duplicates
        entities = {k: list(set(v)) for k, v in entities.items()}
        
        # Add rule-based dish extraction (prioritize this)
        rule_dishes = self.extract_dishes_by_rules(text)
        entities['dishes'].extend(rule_dishes)
        
        # Remove duplicates (case-insensitive)
        seen = set()
        unique_dishes = []
        for dish in entities['dishes']:
            dish_lower = dish.lower()
            if dish_lower not in seen:
                seen.add(dish_lower)
                unique_dishes.append(dish)
        entities['dishes'] = unique_dishes
        
        return entities
    
    def extract_dishes_by_rules(self, text: str) -> List[str]:
        """
        Extract dish names using regex patterns
        
        Args:
            text: Review text
            
        Returns:
            List of potential dish names
        """
        dishes = set()
        
        # Common Indian dishes
        indian_dishes = [
            'butter chicken', 'chicken tikka', 'tandoori chicken', 'chicken curry',
            'paneer tikka', 'palak paneer', 'dal', 'dal makhani', 'biryani', 
            'samosa', 'naan', 'garlic naan', 'butter naan', 'roti', 'chapati', 
            'paratha', 'tikka masala', 'korma', 'vindaloo', 'doro wat', 'injera',
            'masala dosa', 'idli', 'vada', 'pakora'
        ]
        
        # Common dishes from other cuisines
        common_dishes = [
            # Italian
            'pizza', 'margherita pizza', 'pasta', 'spaghetti', 'lasagna', 
            'fettuccine', 'carbonara', 'alfredo', 'ravioli', 'gnocchi', 'tiramisu',
            'risotto', 'bruschetta', 'parmigiana',
            
            # American
            'burger', 'cheeseburger', 'impossible burger', 'hot dog', 'fries',
            'french fries', 'wings', 'buffalo wings', 'ribs', 'pulled pork',
            'mac and cheese', 'eggs benedict', 'avocado toast', 'milkshake',
            
            # Japanese
            'sushi', 'sashimi', 'ramen', 'tempura', 'teriyaki', 'tonkatsu',
            'udon', 'soba', 'california roll', 'miso soup', 'edamame',
            
            # Mexican
            'taco', 'fish taco', 'burrito', 'quesadilla', 'enchilada', 
            'guacamole', 'nachos', 'fajita', 'tamale', 'churro',
            
            # Chinese
            'dumpling', 'fried rice', 'chow mein', 'dim sum', 'wonton',
            'kung pao chicken', 'sweet and sour', 'peking duck', 'spring roll',
            
            # Korean
            'galbi', 'bulgogi', 'kimchi', 'bibimbap', 'japchae', 'tteokbokki',
            
            # Thai
            'pad thai', 'tom yum', 'green curry', 'red curry', 'papaya salad',
            
            # Others
            'pho', 'banh mi', 'steak', 'filet mignon', 'salad', 'caesar salad',
            'quinoa salad', 'soup', 'sandwich', 'lobster', 'crab', 'shrimp',
            'cheesecake', 'foie gras', 'beef wellington', 'pani puri', 'vada pav',
            'falafel', 'hummus', 'shawarma', 'gyro', 'kebab'
        ]
        
        # Combine all dish keywords
        all_dishes = indian_dishes + common_dishes
        
        text_lower = text.lower()
        
        # Extract dishes by exact keyword matching only
        for dish in all_dishes:
            if f' {dish} ' in f' {text_lower} ' or text_lower.startswith(dish) or text_lower.endswith(dish):
                dishes.add(dish.title())
        
        # Return cleaned list
        return list(dishes)[:10]  # Limit to top 10 dishes
        
        # Remove duplicates and clean
        dishes = [d.strip() for d in dishes if len(d.split()) <= 4]
        return list(set(dishes))[:10]  # Limit to top 10
    
    def extract_with_rules(self, text: str) -> Dict[str, List[str]]:
        """
        Fallback method using rule-based extraction
        
        Args:
            text: Review text
            
        Returns:
            Dictionary with extracted entities
        """
        entities = {
            'dishes': self.extract_dishes_by_rules(text),
            'restaurants': [],
            'locations': [],
            'people': []
        }
        
        return entities
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Main entity extraction method
        
        Args:
            text: Review text
            
        Returns:
            Dictionary with all extracted entities
        """
        if self.spacy_available:
            entities = self.extract_with_spacy(text)
        else:
            entities = self.extract_with_rules(text)
        
        # Filter out common words and clean results
        entities = self._clean_entities(entities)
        
        return entities
    
    def _clean_entities(self, entities: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """Clean and filter extracted entities"""
        # Common words to exclude
        stopwords = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at',
            'very', 'good', 'great', 'best', 'nice', 'amazing'
        }
        
        cleaned = {}
        for entity_type, entity_list in entities.items():
            # Remove stopwords and short entities
            filtered = [
                e for e in entity_list 
                if e.lower() not in stopwords and len(e) > 2
            ]
            cleaned[entity_type] = filtered[:10]  # Limit to 10 per type
        
        return cleaned
    
    def get_summary(self, text: str) -> Dict[str, int]:
        """
        Get count summary of entities
        
        Args:
            text: Review text
            
        Returns:
            Dictionary with entity counts
        """
        entities = self.extract_entities(text)
        return {
            entity_type: len(entity_list)
            for entity_type, entity_list in entities.items()
            if entity_list
        }


# Test function
if __name__ == "__main__":
    recognizer = EntityRecognizer()
    
    test_review = """
    I visited Olive Garden in downtown Chicago last night. 
    The Chicken Alfredo and Caesar Salad were absolutely delicious.
    Our waiter John was very attentive and friendly.
    I also tried their famous Tiramisu for dessert.
    """
    
    print("Testing Entity Recognizer\n" + "="*50)
    print(f"Review: {test_review.strip()}\n")
    
    entities = recognizer.extract_entities(test_review)
    
    print("Extracted Entities:")
    for entity_type, entity_list in entities.items():
        if entity_list:
            print(f"\n{entity_type.title()}:")
            for entity in entity_list:
                print(f"  • {entity}")
