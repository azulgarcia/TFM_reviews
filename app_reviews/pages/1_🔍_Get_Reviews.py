import streamlit as st
from app_reviews.other_functions import obtain_reviews_to_csv
from app_reviews.openai_integration.openai_api import get_answer_review
from app_reviews.vector_database.frequent_answers import get_frequent_answer
from app_reviews.translate_answer.functions_translate import translate_text_en, translate_text_fr, translate_text_de

st.title("TripAdvisor Reviews")

if 'obtain_reviews_button_pressed' not in st.session_state:
    st.session_state.obtain_reviews_button_pressed = False

if 'review_index' not in st.session_state:
    st.session_state.review_index = 0

if 'translate_review_answer' not in st.session_state:
    st.session_state.translate_review_answer = False

if not st.session_state.obtain_reviews_button_pressed:
    if st.button("Get Reviews"):
        st.session_state.obtain_reviews_button_pressed = True
        st.session_state.df = obtain_reviews_to_csv()
        st.session_state.review_index = 0
        st.empty()

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
            response = response.split("SOURCES:")[0].strip()
            st.write(f"**Suggested answer:** {response}")

        obtain_frequent_responses = st.checkbox(f"Get Frequently Answered - Review {review_index + 1}")
        if obtain_frequent_responses:
            frequent_responses = get_frequent_answer("answer_2", df['body'][review_index])

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
