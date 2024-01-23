import pandas as pd
import spacy
from app_reviews.vector_database.functions_database import get_all_reviews, connect_to_qdrant
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


client = connect_to_qdrant()
df = get_all_reviews(client,"reviews")

df_features = df['body'].apply(identify_features).apply(pd.Series)

df_reviews = pd.concat([df, df_features], axis=1)

df_sentiments = df_reviews.groupby('sentiment_label').agg({
    'comida': 'sum',
    'servicio': 'sum',
    'precio': 'sum'
}).reset_index()

print(df_sentiments)

import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 4))
ax.axis('tight')
ax.axis('off')
ax.table(cellText=df_sentiments.values, colLabels=df_sentiments.columns, cellLoc='center', loc='center')

plt.show()