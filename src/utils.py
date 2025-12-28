"""
Utility functions for the Restaurant Review Analyzer
"""

import re
import string
import contractions
from typing import List, Dict
import pandas as pd


def clean_text(text: str) -> str:
    """
    Clean and preprocess text data
    
    Args:
        text: Raw review text
        
    Returns:
        Cleaned text
    """
    # Convert to lowercase
    text = text.lower()
    
    # Expand contractions (don't -> do not)
    text = contractions.fix(text)
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text.strip()


def remove_punctuation(text: str) -> str:
    """Remove punctuation from text"""
    return text.translate(str.maketrans('', '', string.punctuation))


def get_rating_category(rating: float) -> str:
    """
    Convert numerical rating to sentiment category
    
    Args:
        rating: Rating value (1-5)
        
    Returns:
        Sentiment category: positive, neutral, negative
    """
    if rating >= 4:
        return 'positive'
    elif rating >= 3:
        return 'neutral'
    else:
        return 'negative'


def extract_sentences(text: str) -> List[str]:
    """
    Split text into sentences
    
    Args:
        text: Input text
        
    Returns:
        List of sentences
    """
    # Simple sentence splitting (can be improved with spaCy)
    sentences = re.split(r'[.!?]+', text)
    return [s.strip() for s in sentences if s.strip()]


def calculate_metrics(y_true: List, y_pred: List) -> Dict[str, float]:
    """
    Calculate classification metrics
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        
    Returns:
        Dictionary with accuracy, precision, recall, f1
    """
    from sklearn.metrics import accuracy_score, precision_recall_fscore_support
    
    accuracy = accuracy_score(y_true, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, average='weighted', zero_division=0
    )
    
    return {
        'accuracy': round(accuracy, 4),
        'precision': round(precision, 4),
        'recall': round(recall, 4),
        'f1_score': round(f1, 4)
    }


def format_output(results: Dict) -> str:
    """
    Format analysis results for display
    
    Args:
        results: Dictionary containing analysis results
        
    Returns:
        Formatted string output
    """
    output = []
    output.append("=" * 50)
    output.append("RESTAURANT REVIEW ANALYSIS")
    output.append("=" * 50)
    
    if 'sentiment' in results:
        output.append(f"\n📊 Overall Sentiment: {results['sentiment'].upper()}")
        if 'sentiment_score' in results:
            output.append(f"   Confidence: {results['sentiment_score']:.2%}")
    
    if 'aspects' in results and results['aspects']:
        output.append("\n🔍 Aspect Analysis:")
        for aspect, sentiment in results['aspects'].items():
            output.append(f"   • {aspect.title()}: {sentiment}")
    
    if 'cuisine' in results:
        output.append(f"\n🍽️  Cuisine Type: {results['cuisine'].title()}")
    
    if 'entities' in results and results['entities']:
        output.append("\n📝 Extracted Entities:")
        for entity_type, entities in results['entities'].items():
            if entities:
                output.append(f"   • {entity_type}: {', '.join(entities)}")
    
    output.append("\n" + "=" * 50)
    
    return "\n".join(output)


def save_results(results: pd.DataFrame, filename: str):
    """Save analysis results to CSV"""
    results.to_csv(filename, index=False)
    print(f"✅ Results saved to {filename}")


def load_sample_reviews() -> List[Dict]:
    """
    Load sample restaurant reviews for testing
    
    Returns:
        List of sample review dictionaries
    """
    samples = [
        {
            "text": "The pasta was absolutely delicious! Great atmosphere and excellent service. A bit pricey but totally worth it.",
            "rating": 5,
            "cuisine": "Italian"
        },
        {
            "text": "Food was okay but the service was terrible. We waited 45 minutes for our order. Not coming back.",
            "rating": 2,
            "cuisine": "American"
        },
        {
            "text": "Amazing Indian food! The butter chicken and naan were perfect. Friendly staff and cozy ambiance.",
            "rating": 5,
            "cuisine": "Indian"
        },
        {
            "text": "Decent sushi but overpriced. The place was clean and service was fast though.",
            "rating": 3,
            "cuisine": "Japanese"
        },
        {
            "text": "Worst Mexican food ever. Tacos were cold and flavorless. Very disappointing experience.",
            "rating": 1,
            "cuisine": "Mexican"
        }
    ]
    return samples
