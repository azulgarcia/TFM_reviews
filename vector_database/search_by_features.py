from sentence_transformers import SentenceTransformer
import numpy as np
from vector_database.functions_database import connect_to_qdrant, search_reviews

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_reviews_by_features(feature):

    if feature == "Food":
        feature_keywords = ["comida", "menú", "plato", "sabor", "delicioso"]
    elif feature == "Service":
        feature_keywords = ["servicio", "camareros", "atención", "personal", "tiempos", "trato"]
    elif feature == "Price":
        feature_keywords = ["precio"]

    embeddings = []
    for word in feature_keywords:
        embeddings.append(model.encode(word))

    embeddings_array = np.array(embeddings)
    embeddings_characteristics = np.mean(embeddings_array, axis=0).tolist()
    client = connect_to_qdrant()
    collection_name = "reviews"
    hits = search_reviews(client, collection_name, embeddings_characteristics)

    return hits

'''
# test:
reviews_food = get_reviews_by_features("Food")
print("food:")
for hit in reviews_food:
    print(hit.score, hit.payload["body"])

reviews_service = get_reviews_by_features("Service")
print("service:")
for hit in reviews_service:
    print(hit.score, hit.payload["body"])


reviews_price = get_reviews_by_features("Price")
print("price:")
for hit in reviews_price:
    print(hit.score, hit.payload["body"])
'''
