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
    hits = search_reviews(client, embeddings_characteristics)

    return hits

