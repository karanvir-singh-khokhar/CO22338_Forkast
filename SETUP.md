# Project Setup Guide

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Download spaCy Model
```bash
python -m spacy download en_core_web_sm
```

### 3. Run the Application
```bash
streamlit run app/streamlit_app.py
```

## Detailed Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Internet connection (for downloading models)

### Step-by-Step Installation

1. **Create Virtual Environment (Recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Mac/Linux
   source venv/bin/activate
   ```

2. **Install Required Packages**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Download NLP Models**
   ```bash
   # Download spaCy English model
   python -m spacy download en_core_web_sm
   
   # Download NLTK data (if needed)
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
   ```

4. **Test Individual Modules**
   ```bash
   # Test sentiment analyzer
   python src/sentiment_analyzer.py
   
   # Test aspect detector
   python src/aspect_detector.py
   
   # Test cuisine classifier
   python src/cuisine_classifier.py
   
   # Test entity recognizer
   python src/entity_recognition.py
   ```

5. **Launch Web Application**
   ```bash
   streamlit run app/streamlit_app.py
   ```
   
   The app will open in your browser at `http://localhost:8501`

## Dataset Setup (Optional)

### Using Yelp Open Dataset

1. **Download Dataset**
   - Visit: https://www.yelp.com/dataset
   - Download the JSON files
   - Extract to `data/raw/` folder

2. **Process Dataset**
   ```bash
   python src/data_preprocessing.py
   ```

### Using Sample Data

The application includes built-in sample reviews for testing. No dataset download required for basic functionality.

## Troubleshooting

### Common Issues

1. **spaCy model not found**
   ```bash
   python -m spacy download en_core_web_sm
   ```

2. **Module not found errors**
   - Ensure you're in the project root directory
   - Check virtual environment is activated
   - Reinstall requirements: `pip install -r requirements.txt`

3. **Port already in use (Streamlit)**
   ```bash
   streamlit run app/streamlit_app.py --server.port 8502
   ```

4. **Torch installation issues on Windows**
   ```bash
   pip install torch --index-url https://download.pytorch.org/whl/cpu
   ```

## Project Structure

```
NLP Project Section B/
├── app/
│   └── streamlit_app.py       # Web interface
├── src/
│   ├── sentiment_analyzer.py  # Sentiment analysis
│   ├── aspect_detector.py     # Aspect extraction
│   ├── cuisine_classifier.py  # Cuisine classification
│   ├── entity_recognition.py  # Named entity recognition
│   └── utils.py               # Helper functions
├── data/                      # Dataset folder
├── models/                    # Saved models
├── requirements.txt           # Dependencies
└── README.md                  # Documentation
```

## Features

### Implemented NLP Techniques

1. **Sentiment Analysis**
   - Overall review sentiment (positive/negative/neutral)
   - Confidence scoring
   - TextBlob and Transformer options

2. **Aspect-Based Sentiment**
   - Food quality analysis
   - Service evaluation
   - Ambiance assessment
   - Price/value perception

3. **Cuisine Classification**
   - 8+ cuisine types supported
   - Keyword-based matching
   - Confidence scoring

4. **Entity Recognition**
   - Dish name extraction
   - Restaurant identification
   - Location detection
   - Person name extraction

## Next Steps

1. Test the application with sample reviews
2. Explore each NLP module individually
3. Download Yelp dataset for larger scale testing
4. Customize and extend features as needed

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review module documentation in source files
3. Test individual modules before running full app

## License

Educational project for NLP coursework.
