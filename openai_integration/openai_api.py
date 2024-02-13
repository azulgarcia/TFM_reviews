import openai
import os
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
GPT_MODEL = "gpt-3.5-turbo"

def get_answer_review(review):
    prompt = "¿Puedes proporcionar una respuesta sugerida para que el dueño del restaurante pueda responder de " \
              "manera efectiva a la reseña en TripAdvisor? Ten en cuenta que la respuesta debe ser profesional, " \
              "agradecida y abordar cualquier problema mencionado en la reseña de manera proactiva: \n"

    prompt_request = prompt + review

    response = openai.ChatCompletion.create(
      messages=[
        {
          "role": "user",
          "content": prompt_request,
        }
      ],
      model=GPT_MODEL,
      temperature=0,
      max_tokens=100,
      stop="\n"
    )

    return response.choices[0]["message"]["content"]

