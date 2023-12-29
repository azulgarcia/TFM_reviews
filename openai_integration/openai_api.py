from langchain import OpenAI
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.schema import Document
import os

GPT_MODEL = "gpt-3.5-turbo"
api_key = "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"
#api_key = os.environ.get('API_KEY_OPENAI')

llm = OpenAI(openai_api_key=api_key)

def get_doc_from_text(text, index=1):
    metadata = {"source": f"Review from TripAdvisor - {index}"}
    return Document(page_content=text, metadata=metadata)

def get_answer_review(review):
    single_review = review
    document = get_doc_from_text(single_review)
    chain = load_qa_with_sources_chain(llm=llm)
    query = "¿Puedes proporcionar una respuesta sugerida para que el dueño del restaurante pueda responder de " \
            "manera efectiva a la reseña en TripAdvisor? Ten en cuenta que la respuesta debe ser profesional, " \
            "agradecida y abordar cualquier problema mencionado en la reseña de manera proactiva."
    res = chain({"question": query, "input_documents": [document]})
    return res["output_text"]

'''
# test
# read a single review
df = pd.read_csv('/get_reviews/data/reviews_tripadvisor.csv')
single_review = df['body'][0]  

# document from the review
document = get_doc_from_text(single_review)

# chain of questions and answers
chain = load_qa_with_sources_chain(llm=llm)

# ask
query = "¿Puedes proporcionar una respuesta sugerida para que el dueño del restaurante pueda responder de manera efectiva a la reseña en TripAdvisor? Ten en cuenta que la respuesta debe ser profesional, agradecida y abordar cualquier problema mencionado en la reseña de manera proactiva."

# answer for the only review
res = chain({"question": query, "input_documents": [document]})

print(res)

print("Respuesta para la reseña:", res["output_text"])
print("Reseña:", single_review)
print("Pregunta:", query)
'''