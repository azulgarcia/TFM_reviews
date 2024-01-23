from app_reviews.vector_database.functions_database import connect_to_qdrant
from sentence_transformers import SentenceTransformer


def get_frequent_answer(collection_name, review):
    qdrant_client = connect_to_qdrant()
    model = SentenceTransformer("all-MiniLM-L6-v2")

    embedding = model.encode(review).tolist()

    hits = qdrant_client.search(
        collection_name=collection_name,
        query_vector=embedding,
        limit=3
    )

    for hit in hits:
        print(hit)

    qdrant_client.close()

    frequent_responses = [hit.payload['answer'] for hit in hits if 'answer' in hit.payload]

    return frequent_responses

'''
###################################################################################################################
# loader frequent answer to Qdrant Cloud
###################################################################################################################
qdrant_client = connect_to_qdrant()
collection_name = "frequent_answer"

model = SentenceTransformer("all-MiniLM-L6-v2")

df = pd.read_csv("C:/Users/Azul/Desktop/TFM/TFM_reviews/vector_database/frequent_answer.csv")
print(df.columns)

questions = df["review"].tolist()

df["encoded"] = model.encode(questions).tolist()

create_collection(qdrant_client, collection_name)
upsert_qdrant(qdrant_client, collection_name, df)

print(qdrant_client.count(collection_name=collection_name))

'''

#test
collection_name = "frequent_answer"
review = "Nos ha gustado mucho, hemos venido un grupo de amigas y la atención, la comida y el trato ha sido muy " \
         "bueno. Marina la camarera ha sido muy amable y atenta, repetiremos seguro"
frequent_responses = get_frequent_answer(collection_name, review)

for i, response in enumerate(frequent_responses, 1):
    print(f"{i}. {response}")

