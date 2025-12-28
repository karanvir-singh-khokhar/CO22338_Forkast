# Restaurant Review Analyzer 🍽️

## Project Description
A real-time NLP application that analyzes restaurant reviews using the Yelp Open Dataset. The system provides comprehensive insights including sentiment analysis, aspect-based feedback, cuisine classification, and entity recognition.

## Features

### Core NLP Tasks (Section B Coverage)
1. **Sentiment Analysis** - Classify reviews as positive, negative, or neutral
2. **Aspect-Based Sentiment** - Extract opinions about:
   - Food Quality
   - Service
   - Ambiance
   - Price/Value
3. **Cuisine Classification** - Identify cuisine type (Indian, Chinese, Italian, Mexican, etc.)
4. **Named Entity Recognition** - Extract dish names, restaurant features
5. **Complaint vs Praise Detection** - Categorize review intent

## Dataset
- **Name**: Yelp Open Dataset
- **Size**: 6M+ reviews
- **Source**: https://www.yelp.com/dataset
- **Format**: JSON files containing business, reviews, and user data

## Technology Stack
- **Language**: Python 3.8+
- **NLP Libraries**: spaCy, NLTK, TextBlob, transformers
- **ML Framework**: scikit-learn
- **Web Framework**: Streamlit (for real-time interface)
- **Data Processing**: pandas, numpy
- **Visualization**: matplotlib, plotly

## Project Structure
```
NLP Project Section B/
│
├── data/                      # Dataset folder
│   ├── raw/                   # Raw Yelp JSON files
│   └── processed/             # Processed data
│
├── models/                    # Trained models
│   ├── sentiment_model.pkl
│   ├── cuisine_classifier.pkl
│   └── aspect_extractor.pkl
│
├── src/                       # Source code
│   ├── data_preprocessing.py  # Data loading and cleaning
│   ├── sentiment_analyzer.py  # Sentiment analysis module
│   ├── aspect_detector.py     # Aspect extraction module
│   ├── cuisine_classifier.py  # Cuisine classification
│   ├── entity_recognition.py  # NER module
│   └── utils.py               # Helper functions
│
├── app/                       # Web application
│   └── streamlit_app.py       # Real-time interface
│
├── notebooks/                 # Jupyter notebooks for exploration
│   └── exploratory_analysis.ipynb
│
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Section B Syllabus Coverage

### ✅ Semantic Interpretation
- Sentiment analysis (lexical semantics)
- Aspect-based sentiment (linking syntax and semantics)

### ✅ NLP Concepts
- Named entity recognition (dishes, restaurants)
- Text classification (sentiment, cuisine, intent)

### ✅ Syntactic Processing
- Part-of-speech tagging for aspect extraction
- Dependency parsing for opinion mining

## Installation & Setup

1. Clone/navigate to project directory
2. Install dependencies: `pip install -r requirements.txt`
3. Download spaCy model: `python -m spacy download en_core_web_sm`
4. Download Yelp dataset from official website
5. Run preprocessing: `python src/data_preprocessing.py`
6. Launch app: `streamlit run app/streamlit_app.py`

## Usage
1. Upload or paste a restaurant review
2. Get instant analysis with:
   - Overall sentiment score
   - Aspect-wise breakdown
   - Identified cuisine type
   - Extracted entities (dishes, features)

## Future Enhancements
- Multi-language support
- Review summarization
- Recommendation system based on user preferences
- Fake review detection

~ Web App Link: 