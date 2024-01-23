from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import pandas as pd
from sentence_transformers import SentenceTransformer


def connect_to_qdrant():

    qdrant_client = QdrantClient(
        url="https://0ec4558e-754e-49d3-8ac3-658d0a498955.us-east4-0.gcp.cloud.qdrant.io:6333",
        api_key="0fhGp_s_vA1xP9TIdGGTRiAXnnGjeUdTKP6vtsYITcGehdYykGZ4pg",
    )

    return qdrant_client

def create_collection(qdrant_client,collection_name):
    qdrant_client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )
    return f"created collection: {collection_name}"

def upsert_qdrant(qdrant_client,collection_name, df):
    qdrant_client.upsert(
        collection_name=collection_name,
        points=[
            PointStruct(
                id=idx,
                vector=row["encoded"],
                payload={"answer": (row["answer"])},
            )
            for idx, row in df.iterrows()
        ],
    )

    return print("Number of answers", qdrant_client.count(collection_name=collection_name))

def upsert_reviews(client, collection, df):

    model = SentenceTransformer("all-MiniLM-L6-v2")

    reviews = df['body'].tolist()
    df["encoded"] = model.encode(reviews).tolist()

    payload = df.to_dict(orient="records")

    client.upsert(
        collection_name=collection,
        points=[
            PointStruct(
                id=idx,
                vector=row['encoded'],
                payload=payload[idx]
            )
            for idx, row in df.iterrows()
        ]
    )


def search_reviews(client, collection, query_vector):

    search_result = client.search(
        collection_name=collection,
        query_vector=query_vector,
    )
    return search_result


def get_all_reviews(client, collection):

    search_result = client.search(
        collection_name=collection,
        query_vector=[0.0] * 384,
        limit=100
    )

    metadata = []

    for scored_point in search_result:
        payload_data = scored_point.payload
        metadata.append(payload_data)

    df = pd.DataFrame(metadata)

    return df

def get_all_reviews_2(client, collection):
    search_result = client.search(
        collection_name=collection,
        query_vector=[0.0] * 384,
        limit=100,
    )

    return search_result
