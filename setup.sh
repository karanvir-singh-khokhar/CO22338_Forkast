#!/bin/bash

# Download spaCy model for English
python -m spacy download en_core_web_sm --quiet

# Download NLTK data
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True)"

