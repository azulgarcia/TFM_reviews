import streamlit as st
from other_functions import obtain_reviews_to_csv
from openai_integration.openai_api import get_answer_review
from vector_database.frequent_answers import get_frequent_answer
from translate_answer.functions_translate import translate_text

st.markdown(
"""
    TODO
    - modify function to get reviews
    - unchecking the "frequent answers" checkbox when changing reviews
"""
)

st.title("TripAdvisor Reviews")

if 'obtain_reviews_button_pressed' not in st.session_state:
    st.session_state.obtain_reviews_button_pressed = False

if 'review_index' not in st.session_state:
    st.session_state.review_index = 0
    st.session_state.obtain_frequent_responses = False

if 'review_index' not in st.session_state:
    st.session_state.review_index = 0
    st.session_state.translate_review_answer = False  #


if not st.session_state.obtain_reviews_button_pressed:
    if st.button("Get Reviews"):
        st.session_state.df = obtain_reviews_to_csv()
        st.session_state.obtain_reviews_button_pressed = True
        st.session_state.review_index = 0
        st.empty()

if 'df' in st.session_state:
    df = st.session_state.df

    review_index = st.session_state.review_index

    st.markdown(
        """
        <div style="border: 2px solid #e5e5e5; border-radius: 5px; padding: 10px;">
            <p><strong>Título:</strong> {title}</p>
            <p><strong>Autor:</strong> {author}</p>
            <p><strong>Fecha de visita:</strong> {date}</p>
            <p><strong>Puntuación:</strong> {score}</p>
            <p><strong>Cuerpo:</strong> {body}</p>
            <p><a href="{link}" target="_blank">Ver reseña en TripAdvisor</a></p>
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

    if st.button("Next Review"):
        st.session_state.review_index = (st.session_state.review_index + 1) % len(df)
        st.session_state.obtain_frequent_responses = False

    if st.button("Get Custom Answer"):
        response = get_answer_review(df['body'][review_index])

        response = response.split("SOURCES:")[0].strip()

        st.write(f"**Suggested answer:** {response}")

    st.session_state.obtain_frequent_responses = st.checkbox("Get Frequently Answered", st.session_state.obtain_frequent_responses)

    if st.session_state.obtain_frequent_responses:
        frequent_responses = get_frequent_answer("answer_2", df['body'][review_index])

        st.write("**Frequent answer:**")
        for i, response in enumerate(frequent_responses, 1):
            st.markdown(f"{i}. {response}", unsafe_allow_html=True)

            translate_button_clicked = st.checkbox(f"Translate {i}")

            if translate_button_clicked:
                translated_text = translate_text(response)
                st.markdown(f"**English translation:** {translated_text}")
