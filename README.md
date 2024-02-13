# Representation and analysis of customer opinion

## Description
This project is a comprehensive solution for managing and analyzing TripAdvisor reviews. 

### Main Features

- **get_reviews**: automate the review collection process using web scrcaping techniques.
- **vector_database**: uses qdrant cloud to store the vector representations of the reviews and their metadata and then retrieve them according to different criteria using vector search.
- **sentimental_analysis**: use the BERT model to analyze sentiment from user reviews.
- **openai_integration**: uses the gpt 3.5 model to generate personalized responses to reviews.
- **translate_answer**: uses Hugging Face's Helsinki-NLP models to translate responses into different languages.


## Installation and configuration

Install dependencies in your virtual environment
```bash
pip install -r requirements.txt
```

Fill in environment variables in the .env file
```bash
URL_ESTABLISHMENT= 'property Tripadvisor URL'
URL_QDRANT= 'endpoint Qdrant Cloud'
API_KEY_QDRANT= 'your Qdrant API Key'
COLLECTION_NAME= 'collection name in Qdrant'
OPENAI_API_KEY= 'your OpenAI API Key'
```

## Use

```bash
streamlit run  🏡_Home.py
```

