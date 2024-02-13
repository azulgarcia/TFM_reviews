import os
from qdrant_client.models import VectorParams, Distance, PointStruct
from sentence_transformers import SentenceTransformer
import pandas as pd
from qdrant_client import QdrantClient

'''
You can use this script to upload to your Qdrant Cloud database from a .csv file. The file must contain:
- page_number
- date
- title
- body
- author
- score
- link
- sentiment_label
- sentiment_score

This file structure is generated with the script reviews_tripadvisor.py
'''

COLLECTION = os.getenv('COLECTION_NAME')
URL_QDRANT = os.getenv('URL_QDRANT')
API_KEY_QDRANT = os.getenv('API_KEY_QDRANT')

df = pd.read_csv("/app_reviews/sentimental_analysis/reviews_tripadvisor_with_sentiment.csv")
model = SentenceTransformer("all-MiniLM-L6-v2")
reviews = df['body'].tolist()
df["encoded"] = model.encode(reviews).tolist()
payload = df.to_dict(orient="records")

##############################################################################################################
# Qdrant cloud
##############################################################################################################

qdrant_client = QdrantClient(
    url=URL_QDRANT,
    api_key=API_KEY_QDRANT,
)

qdrant_client.recreate_collection(
    collection_name=COLLECTION,
    vectors_config=VectorParams(size=384, distance=Distance.COSINE),
)

qdrant_client.upsert(
    collection_name=COLLECTION,
    points=[
        PointStruct(
            id=idx,
            vector=row['encoded'],  # Accede al vector de la fila actual
            payload=payload[idx]
        )
        for idx, row in df.iterrows()
    ]
)


