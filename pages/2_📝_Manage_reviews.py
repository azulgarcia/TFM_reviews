import streamlit as st
import pandas as pd
from openai_integration.openai_api import get_answer_review
from vector_database.frequent_answers import get_frequent_answer
from vector_database.functions_database import connect_to_qdrant, upsert_reviews
from sentimental_analysis.sentiment_features import identify_features
from sentimental_analysis.sentiment_analysis_transf import sentimental_analysis_to_df
from translate_answer.functions_translate import translate_text_en, translate_text_fr, translate_text_de

def main():
    st.title("Manage TripAdvisor Reviews")

    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    if 'review_index' not in st.session_state:
        st.session_state.review_index = 0

    if 'translate_review_answer' not in st.session_state:
        st.session_state.translate_review_answer = False

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        # sentimental analysis and upsert to qdrant
        df_with_sentiment = sentimental_analysis_to_df(df)
        df_features = df_with_sentiment['body'].apply(identify_features).apply(pd.Series)
        df_reviews_final = pd.concat([df_with_sentiment, df_features], axis=1)
        client = connect_to_qdrant()
        upsert_reviews(client, df_reviews_final)
        st.session_state.df = df

    if 'df' in st.session_state:
            df = st.session_state.df

            for review_index in range(len(df)):
                st.markdown(
                    """
                    <div style="border: 2px solid #e5e5e5; border-radius: 5px; padding: 10px;">
                        <p><strong>Title:</strong> {title}</p>
                        <p><strong>Author:</strong> {author}</p>
                        <p><strong>Visit date:</strong> {date}</p>
                        <p><strong>Score:</strong> {score}</p>
                        <p><strong>Review:</strong> {body}</p>
                        <p><a href="{link}" target="_blank">Go to the review</a></p>
                    </div>
                    """.format(
                        title=df['title'][review_index],
                        author=df['author'][review_index],
                        date=df['date'][review_index],
                        score=df['score'][review_index],
                        body=df['body'][review_index],
                        link=df['link'][review_index]
                    ),
                    unsafe_allow_html=True
                )

                get_custom_answer_clicked = st.button(f"Get Custom Answer - Review {review_index + 1}")
                if get_custom_answer_clicked:
                    response = get_answer_review(df['body'][review_index])
                    st.write(f"**Suggested answer:** {response}")

                obtain_frequent_responses = st.checkbox(f"Get Frequently Answered - Review {review_index + 1}")

                if obtain_frequent_responses:
                    frequent_responses = get_frequent_answer(df['body'][review_index])

                    st.write("**Frequent answer:**")
                    for i, response in enumerate(frequent_responses, 1):
                        st.markdown(f"{i}. {response}", unsafe_allow_html=True)

                        checkboxes = st.columns(3)
                        translate_button_clicked_en = checkboxes[0].checkbox(f"Translate english {i}")
                        translate_button_clicked_fr = checkboxes[1].checkbox(f"Translate french {i}")
                        translate_button_clicked_de = checkboxes[2].checkbox(f"Translate german {i}")

                        if translate_button_clicked_en:
                            translated_text = translate_text_en(response)
                            st.markdown(f"**English translation:** {translated_text}")

                        if translate_button_clicked_fr:
                            translated_text = translate_text_fr(response)
                            st.markdown(f"**French translation:** {translated_text}")

                        if translate_button_clicked_de:
                            translated_text = translate_text_de(response)
                            st.markdown(f"**German translation:** {translated_text}")

if __name__ == "__main__":
    main()
