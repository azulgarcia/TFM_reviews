import pandas as pd
import spacy
import os
from vector_database.functions_database import get_all_reviews, connect_to_qdrant
from dotenv import load_dotenv

load_dotenv()

COLLECTION = os.getenv('COLLECTION_NAME')


def identify_features(text):
    nlp = spacy.load("es_core_news_sm")

    features = {
        "comida": ["comida", "plato", "menú", "sabor"],
        "servicio": ["servicio", "atención", "mesero", "amabilidad"],
        "precio": ["precio", "costo", "tarifa", "valor"]
    }

    doc = nlp(text)

    presence_features = {feature: 0 for feature in features}

    for feature, keywords in features.items():
        for word in keywords:
            if word in [token.text.lower() for token in doc]:
                presence_features[feature] = 1
                break

    return presence_features


def get_sentiment_features(client):
    df = get_all_reviews(client)
    df_features = df['body'].apply(identify_features).apply(pd.Series)

    df_reviews = pd.concat([df, df_features], axis=1)

    df_sentiments = df_reviews.groupby('sentiment_label').agg({
        'comida': 'sum',
        'servicio': 'sum',
        'precio': 'sum'
    }).reset_index()

    return df_sentiments
