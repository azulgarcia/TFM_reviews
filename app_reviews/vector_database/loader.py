from qdrant_client.models import VectorParams, Distance, PointStruct
from sentence_transformers import SentenceTransformer
import pandas as pd
from qdrant_client import QdrantClient

df = pd.read_csv("/app_reviews/sentimental_analysis/reviews_tripadvisor_with_sentiment.csv")

model = SentenceTransformer("all-MiniLM-L6-v2")

reviews = df['body'].tolist()
df["encoded"] = model.encode(reviews).tolist()

payload = df.to_dict(orient="records")

##############################################################################################################
# Qdrant cloud
##############################################################################################################

qdrant_client = QdrantClient(
    url="https://0ec4558e-754e-49d3-8ac3-658d0a498955.us-east4-0.gcp.cloud.qdrant.io:6333",
    api_key="0fhGp_s_vA1xP9TIdGGTRiAXnnGjeUdTKP6vtsYITcGehdYykGZ4pg",
)

qdrant_client.recreate_collection(
    collection_name="reviews",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE),
)

qdrant_client.upsert(
    collection_name="reviews",
    points=[
        PointStruct(
            id=idx,
            vector=row['encoded'],  # Accede al vector de la fila actual
            payload=payload[idx]
        )
        for idx, row in df.iterrows()
    ]
)


