# Representation and analysis of customer opinion

## Description
This project is a comprehensive solution for the management and analysis of TripAdvisor restaurant reviews. 

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
COLLECTION_NAME= 'name for the reviews collection in Qdrant'
COLLECTION_FREQUENT_ANSWER= 'name for the collection of frequently reviews answers in Qdrant'
OPENAI_API_KEY= 'your OpenAI API Key'
FILE_FREQUENT_ANSWER= 'file name with reviews and frequent answers'
```

Generate the collection for reviews and generate and load the collection with frequent answers. You can generate a personalized one according to the establishment you choose or use the generic one from this project.
the file should be saved in the directory '/TFM_reviews'.

```bash
python -m db_create.py
```

## Use

```bash
streamlit run  🏡_Home.py
```

