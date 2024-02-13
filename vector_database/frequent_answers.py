from vector_database.functions_database import connect_to_qdrant
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv

load_dotenv()

COLLECTION = os.getenv('COLLECTION_NAME')
def get_frequent_answer(review):
    qdrant_client = connect_to_qdrant()
    model = SentenceTransformer("all-MiniLM-L6-v2")

    embedding = model.encode(review).tolist()

    hits = qdrant_client.search(
        collection_name=COLLECTION,
        query_vector=embedding,
        limit=3
    )

    for hit in hits:
        print(hit)

    qdrant_client.close()

    frequent_responses = [hit.payload['answer'] for hit in hits if 'answer' in hit.payload]

    return frequent_responses

