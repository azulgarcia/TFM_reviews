from transformers import MarianMTModel, MarianTokenizer
import streamlit as st
def translate_text(answer):
    modelo = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-es-en")
    tokenizador = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-es-en")

    entrada = tokenizador(answer, return_tensors="pt")
    traduccion_ids = modelo.generate(**entrada)
    traduccion_texto = tokenizador.batch_decode(traduccion_ids, skip_special_tokens=True)[0]

    # Imprimir la traducción
    print(f"Texto original (español): {answer}")
    print(f"Traducción (inglés): {traduccion_texto}")

    return traduccion_texto


#answer = "Lamentamos escuchar que tu experiencia no estuvo a la altura de tus expectativas. Valoramos tu retroalimentación y trabajaremos arduamente para mejorar."
#translate_text(answer)