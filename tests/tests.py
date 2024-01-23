from app_reviews.vector_database.functions_database import connect_to_qdrant, get_all_reviews
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

client = connect_to_qdrant()
df = get_all_reviews(client, "reviews")
#print(reviews_df)

df['score'] = pd.to_numeric(df['score'])

df['sentiment_label'] = df['sentiment_label'].apply(lambda x: 'positive' if '5 stars' in x or '4 stars' in x else 'neutral' if '3 stars' in x else 'negative')

df['predicted_label'] = df['score'].apply(lambda x: 'positive' if x in [4, 5] else 'neutral' if x == 3 else 'negative')

accuracy = accuracy_score(df['sentiment_label'], df['predicted_label'])
print(f'Precisión: {accuracy:.2%}')

print('Informe de Clasificación:')
print(classification_report(df['sentiment_label'], df['predicted_label']))

conf_matrix = confusion_matrix(df['sentiment_label'], df['predicted_label'])
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=['negative', 'neutral', 'positive'], yticklabels=['negative', 'neutral', 'positive'])
plt.xlabel('Predicho')
plt.ylabel('Real')
plt.title('Matriz de Confusión')
plt.show()