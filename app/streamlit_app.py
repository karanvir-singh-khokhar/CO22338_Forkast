"""
Real-Time Restaurant Review Analyzer Web Application
Built with Streamlit for interactive analysis
"""

import streamlit as st
import sys
import os

# Download spaCy model if not available
try:
    import spacy
    spacy.load('en_core_web_sm')
except:
    import subprocess
    subprocess.run(['python', '-m', 'spacy', 'download', 'en_core_web_sm'], check=False)

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from sentiment_analyzer import SentimentAnalyzer, get_sentiment_emoji
from aspect_detector import AspectDetector, get_aspect_emoji
from cuisine_classifier import CuisineClassifier, get_cuisine_emoji
from entity_recognition import EntityRecognizer
from utils import clean_text, load_sample_reviews


# Page configuration
st.set_page_config(
    page_title="Forkast",
    page_icon="🍽️",
    layout="wide"
)


@st.cache_resource
def load_models():
    """Load all NLP models (cached for performance)"""
    sentiment_analyzer = SentimentAnalyzer(method='textblob')
    aspect_detector = AspectDetector()
    cuisine_classifier = CuisineClassifier()
    entity_recognizer = EntityRecognizer()
    
    return sentiment_analyzer, aspect_detector, cuisine_classifier, entity_recognizer


def main():
    """Main application"""
    
    # Title and description
    st.title("🍽️ Forkast - A Restaurant Review Analyzer")
    st.markdown("""
    Analyze restaurant reviews in real-time using advanced NLP techniques!
    Get insights on sentiment, cuisine type, specific aspects, and extracted entities.
    """)
    
    # Load models
    with st.spinner("Loading NLP models..."):
        sentiment_analyzer, aspect_detector, cuisine_classifier, entity_recognizer = load_models()
    
    # Sidebar
    st.sidebar.header("⚙️ Settings")
    
    # Input method selection
    input_method = st.sidebar.radio(
        "Choose input method:",
        ["Enter Custom Review", "Use Sample Reviews"]
    )
    
    # Analysis options
    st.sidebar.subheader("Analysis Options")
    show_sentiment = st.sidebar.checkbox("Sentiment Analysis", value=True)
    show_aspects = st.sidebar.checkbox("Aspect Detection", value=True)
    show_cuisine = st.sidebar.checkbox("Cuisine Classification", value=True)
    show_entities = st.sidebar.checkbox("Entity Recognition", value=True)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📝 Input Review")
        
        if input_method == "Enter Custom Review":
            review_text = st.text_area(
                "Enter a restaurant review:",
                height=150,
                placeholder="Type or paste a restaurant review here..."
            )
        else:
            # Load sample reviews
            samples = load_sample_reviews()
            sample_options = [f"Sample {i+1}: {s['cuisine']}" for i, s in enumerate(samples)]
            selected_sample = st.selectbox("Choose a sample review:", sample_options)
            sample_idx = int(selected_sample.split()[1].replace(':', '')) - 1
            review_text = samples[sample_idx]['text']
            st.text_area("Review:", value=review_text, height=150, disabled=True)
    
    with col2:
        st.subheader("ℹ️ About")
        st.info("""
        **NLP Techniques Used:**
        - Sentiment Analysis
        - Aspect-Based Opinion Mining
        - Cuisine Classification
        - Named Entity Recognition
        
        **Features:**
        ✅ Real-time Analysis
        ✅ Multi-aspect Detection
        ✅ 14+ Cuisine Types
        ✅ Entity Extraction
        """)
    
    # Analyze button
    if st.button("🔍 Analyze Review", type="primary", use_container_width=True):
        if not review_text or len(review_text.strip()) < 10:
            st.error("⚠️ Please enter a valid review (at least 10 characters)")
            return
        
        # Clean text
        cleaned_text = clean_text(review_text)
        
        # Create tabs for results
        tabs = st.tabs(["📊 Overview", "🔍 Detailed Analysis", "📈 Statistics"])
        
        with tabs[0]:  # Overview
            st.subheader("Analysis Results")
            
            # Sentiment Analysis
            if show_sentiment:
                with st.spinner("Analyzing sentiment..."):
                    sentiment_result = sentiment_analyzer.analyze(cleaned_text)
                    
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    emoji = get_sentiment_emoji(sentiment_result['sentiment'])
                    st.metric(
                        "Overall Sentiment",
                        f"{sentiment_result['sentiment'].title()} {emoji}",
                        f"{sentiment_result['confidence']:.1%} confidence"
                    )
                
                # Cuisine Classification
                if show_cuisine:
                    with st.spinner("Classifying cuisine..."):
                        cuisine_result = cuisine_classifier.classify(cleaned_text)
                    
                    with col2:
                        emoji = get_cuisine_emoji(cuisine_result['cuisine'])
                        st.metric(
                            "Cuisine Type",
                            f"{cuisine_result['cuisine']} {emoji}",
                            f"{cuisine_result['confidence']:.1%} confidence"
                        )
                
                # Entity count
                if show_entities:
                    with st.spinner("Extracting entities..."):
                        entities = entity_recognizer.extract_entities(cleaned_text)
                        total_entities = sum(len(v) for v in entities.values())
                    
                    with col3:
                        st.metric(
                            "Entities Extracted",
                            f"{total_entities} items",
                            "dishes, locations, etc."
                        )
            
            # Aspect Analysis
            if show_aspects:
                st.subheader("🎯 Aspect-Based Analysis")
                
                with st.spinner("Analyzing aspects..."):
                    aspects = aspect_detector.get_summary(cleaned_text)
                
                if aspects:
                    cols = st.columns(len(aspects))
                    for idx, (aspect, sentiment) in enumerate(aspects.items()):
                        with cols[idx]:
                            emoji = get_aspect_emoji(sentiment)
                            st.markdown(f"""
                            <div style='text-align: center; padding: 20px; background-color: #1e1e1e; border: 2px solid #333; border-radius: 10px; min-height: 120px; display: flex; flex-direction: column; justify-content: center;'>
                                <h3 style='margin: 0; font-size: 2em;'>{emoji}</h3>
                                <h4 style='margin: 10px 0 5px 0; color: #ffffff; font-weight: bold;'>{aspect.title()}</h4>
                                <p style='margin: 0; color: #a0a0a0; font-size: 0.9em;'>{sentiment.title()}</p>
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.info("No specific aspects mentioned in this review.")
        
        with tabs[1]:  # Detailed Analysis
            st.subheader("Detailed Breakdown")
            
            # Sentiment Details
            if show_sentiment:
                st.markdown("### 😊 Sentiment Analysis")
                st.json(sentiment_result)
            
            # Aspect Details
            if show_aspects:
                st.markdown("### 🎯 Aspect Details")
                full_aspects = aspect_detector.extract_aspects(cleaned_text)
                
                for aspect, data in full_aspects.items():
                    if data['mentioned']:
                        with st.expander(f"{aspect.title()} - {data['sentiment'].title()}"):
                            st.write("**Relevant sentences:**")
                            for sentence in data['sentences']:
                                st.write(f"- {sentence}")
            
            # Cuisine Details
            if show_cuisine:
                st.markdown("### 🍽️ Cuisine Classification")
                all_scores = cuisine_classifier.get_all_scores(cleaned_text)
                if all_scores:
                    st.bar_chart(all_scores)
                else:
                    st.info("Could not determine cuisine type from review.")
            
            # Entity Details
            if show_entities:
                st.markdown("### 📝 Extracted Entities")
                
                if any(entities.values()):
                    for entity_type, entity_list in entities.items():
                        if entity_list:
                            st.write(f"**{entity_type.title()}:**")
                            st.write(", ".join(entity_list))
                else:
                    st.info("No entities extracted from this review.")
        
        with tabs[2]:  # Statistics
            st.subheader("Review Statistics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Word Count", len(review_text.split()))
            
            with col2:
                st.metric("Character Count", len(review_text))
            
            with col3:
                sentences = review_text.count('.') + review_text.count('!') + review_text.count('?')
                st.metric("Sentences", max(1, sentences))
            
            with col4:
                avg_word_length = sum(len(word) for word in review_text.split()) / max(1, len(review_text.split()))
                st.metric("Avg Word Length", f"{avg_word_length:.1f}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🍽️ Forkast | Developed using Streamlit & spaCy</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()