from sentence_transformers import SentenceTransformer
import numpy as np
from vector_database.functions_database import connect_to_qdrant, search_reviews

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_reviews_by_features(feature_keywords):
    embeddings = []
    for word in feature_keywords:
        embeddings.append(model.encode(word))

    embeddings_array = np.array(embeddings)
    embeddings_characteristics = np.mean(embeddings_array, axis=0).tolist()
    client = connect_to_qdrant()
    collection_name = "reviews"
    hits = search_reviews(client, collection_name, embeddings_characteristics)

    for hit in hits:
        print(hit.score, hit.payload["body"])

    return hits

# test:
# keywords
food_keywords = ["comida", "menú", "plato", "sabor", "delicioso"]
service_keywords = ["servicio", "camareros", "atención", "personal", "tiempos", "trato"]
cleaning_keywords = ["limpieza", "limpio", "orden", "sucio", "desorden"]
price_keywords = ["precio"]

reviews_food = get_reviews_by_features(food_keywords)
print("food:")
for hit in reviews_food:
    print(hit.score, hit.payload["body"])

reviews_service = get_reviews_by_features(service_keywords)
print("service:")
for hit in reviews_service:
    print(hit.score, hit.payload["body"])

reviews_cleaning = get_reviews_by_features(cleaning_keywords)
print("cleaning:")
for hit in reviews_cleaning:
    print(hit.score, hit.payload["body"])

reviews_price = get_reviews_by_features(price_keywords)
print("price:")
for hit in reviews_price:
    print(hit.score, hit.payload["body"])


