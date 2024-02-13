from transformers import MarianMTModel, MarianTokenizer

def translate_text_en(answer):
    model_name = "Helsinki-NLP/opus-mt-es-en"
    model = MarianMTModel.from_pretrained(model_name)
    tokenizador = MarianTokenizer.from_pretrained(model_name)

    input = tokenizador(answer, return_tensors="pt")
    translate_ids = model.generate(**input)
    translate_text = tokenizador.batch_decode(translate_ids, skip_special_tokens=True)[0]

    print(f"Original text (spanish): {answer}")
    print(f"Translate (english): {translate_text}")

    return translate_text


def translate_text_fr(answer):
    model_name = "Helsinki-NLP/opus-mt-es-fr"
    model = MarianMTModel.from_pretrained(model_name)
    tokenizador = MarianTokenizer.from_pretrained(model_name)

    input = tokenizador(answer, return_tensors="pt")
    translate_ids = model.generate(**input)
    translate_text = tokenizador.batch_decode(translate_ids, skip_special_tokens=True)[0]

    print(f"Original text (spanish): {answer}")
    print(f"Translate (french): {translate_text}")

    return translate_text

def translate_text_de(answer):
    model_name = "Helsinki-NLP/opus-mt-es-de"
    model = MarianMTModel.from_pretrained(model_name)
    tokenizador = MarianTokenizer.from_pretrained(model_name)

    input = tokenizador(answer, return_tensors="pt")
    translate_ids = model.generate(**input)
    translate_text = tokenizador.batch_decode(translate_ids, skip_special_tokens=True)[0]

    print(f"Original text (spanish): {answer}")
    print(f"Translate (german): {translate_text}")

    return translate_text

