import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv

load_dotenv()

COLLECTION = os.getenv('COLLECTION_NAME')


def connect_to_qdrant():
    qdrant_client = QdrantClient(
        url=os.getenv('URL_QDRANT'),
        api_key=os.getenv('API_KEY_QDRANT')
    )

    return qdrant_client


def create_collection(qdrant_client: object, collection_name: object) -> object:
    qdrant_client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )
    return f"created collection: {collection_name}"


def upsert_reviews(client, df):
    model = SentenceTransformer("all-MiniLM-L6-v2")

    reviews = df['body'].tolist()
    df["encoded"] = model.encode(reviews).tolist()

    payload = df.to_dict(orient="records")

    client.upsert(
        collection_name=COLLECTION,
        points=[
            PointStruct(
                id=idx,
                vector=row['encoded'],
                payload=payload[idx]
            )
            for idx, row in df.iterrows()
        ]
    )


def search_reviews(client, query_vector):
    search_result = client.search(
        collection_name=COLLECTION,
        query_vector=query_vector,
    )
    return search_result


def get_all_reviews(client):
    search_result = client.search(
        collection_name=COLLECTION,
        query_vector=[0.0] * 384,
        limit=100
    )

    metadata = []

    for scored_point in search_result:
        payload_data = scored_point.payload
        metadata.append(payload_data)

    df = pd.DataFrame(metadata)

    return df


def get_all_reviews_2(client):
    search_result = client.search(
        collection_name=COLLECTION,
        query_vector=[0.0] * 384,
        limit=100,
    )

    return search_result
