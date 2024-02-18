import os
from qdrant_client.models import VectorParams, Distance, PointStruct
from qdrant_client import QdrantClient
from dotenv import load_dotenv
import pandas as pd
from sentence_transformers import SentenceTransformer

load_dotenv()

COLLECTION_REVIEW = os.getenv('COLLECTION_NAME')
COLLECTION_FREQUENT_ANSWER = os.getenv('COLLECTION_FREQUENT_ANSWER')
URL_QDRANT = os.getenv('URL_QDRANT')
API_KEY_QDRANT = os.getenv('API_KEY_QDRANT')
FILE_NAME = os.getenv('FILE_FREQUENT_ANSWER')


def main():
    ##############################################################################################################
    # Create review collection in Qdrant Cloud
    ##############################################################################################################

    try:
        qdrant_client = QdrantClient(
            url=URL_QDRANT,
            api_key=API_KEY_QDRANT,
        )

        try:
            qdrant_client.create_collection(
                collection_name=COLLECTION_REVIEW,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE),
            )
            print(f"Created {COLLECTION_REVIEW} collection")

        except:
            print("collection could not be created.")

    except:
        print("Could not connect to Qdrant database.")

    ##############################################################################################################
    # Create frequent answer collection in Qdrant Cloud
    ##############################################################################################################

    df = pd.read_csv(FILE_NAME)
    model = SentenceTransformer("all-MiniLM-L6-v2")
    reviews = df['review'].tolist()
    df["encoded"] = model.encode(reviews).tolist()
    payload = df.to_dict(orient="records")

    try:
        qdrant_client.create_collection(
            collection_name=COLLECTION_FREQUENT_ANSWER,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )
        print(f"Created {COLLECTION_FREQUENT_ANSWER} collection")

        try:
            qdrant_client.upsert(
                collection_name=COLLECTION_FREQUENT_ANSWER,
                points=[
                    PointStruct(
                        id=idx,
                        vector=row['encoded'],
                        payload=payload[idx]
                    )
                    for idx, row in df.iterrows()
                ]
            )
            print("Loaded collection.")

        except:
            print("Collection could not be loaded.")

    except:
        print("collection could not be created.")


if __name__ == "__main__":
    main()
