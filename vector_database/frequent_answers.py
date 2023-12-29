from vector_database.functions_database import connect_to_qdrant, create_collection, upsert_qdrant
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


###################################################################################################################
# loader frequent answer to Qdrant Cloud
###################################################################################################################
qdrant_client = connect_to_qdrant()
collection_name = "answer_2"
'''
df = pd.read_csv("C:/Users/Azul/Desktop/TFM/TFM_reviews/vector_search/frequent_answer.csv")
print(df.columns)

questions = df["review"].tolist()

df["encoded"] = model.encode(questions).tolist()

create_collection(qdrant_client, collection_name)
upsert_qdrant(qdrant_client, collection_name, df)

print(qdrant_client.count(collection_name=collection_name))
'''

#test
review = "Comida buena pero… pedimos 4 platos y 3 de ellos nos los sirvieron al mismo tiempo, en una mesa de 50 cm, malamente nos podíamos mover. El cuarto plato que pedimos se lo pusieron a la mesa de al lado por error, gracias a ello pudimos ganar unos minutos para terminarnos los tres anteriores. A la hora de la cuenta nos pusieron una cerveza de más por error. En resumen la comida está buena pero el resto deja mucho que desear"
frequent_responses = get_frequent_answer(collection_name, review)

print("frequent_responses:")
print(frequent_responses)

print("frequent_responses for:")

for i, response in enumerate(frequent_responses, 1):
    print(f"{i}. {response}")

