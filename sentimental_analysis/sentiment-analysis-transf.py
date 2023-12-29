from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
import pandas as pd
import demoji

model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

df = pd.read_csv('C:/Users/Azul/Desktop/TFM/TFM_reviews/get_reviews/data/reviews_tripadvisor.csv')
reviews = df['body']

# demoji
demoji.download_codes()

df['sentiment_label'] = ''
df['sentiment_score'] = ''

for i, review in enumerate(reviews):
    processed_review = demoji.replace(review, '')

    result = nlp(processed_review)[0]
    sentiment_label = result['label']
    sentiment_score = result['score']

    df.loc[i, 'sentiment_label'] = sentiment_label
    df.loc[i, 'sentiment_score'] = sentiment_score

df.to_csv('reviews_tripadvisor_with_sentiment.csv')
