import streamlit as st
from vector_database.search_by_features import get_reviews_by_features
from vector_database.functions_database import get_all_reviews_2, connect_to_qdrant

def main():
    st.set_page_config(page_title="Historical Reviews", page_icon="📊")

    st.title("Search review by feature")
    characteristics = ["Food", "Service", "Price", "All"]

    selected_feature = st.selectbox("Select feature:", characteristics)

    if st.button("Search"):

        if selected_feature == "All":
            client = connect_to_qdrant()
            hits = get_all_reviews_2(client)
        else:
            hits = get_reviews_by_features(selected_feature)

        for hit in hits:
            st.markdown(
                """
                <div style="border: 2px solid #e5e5e5; border-radius: 5px; padding: 10px;">
                    <p><strong>Date:</strong> {date}</p>
                    <p><strong>Review:</strong> {body}</p>
                    <p><strong>Score:</strong> {score}</p>
                    <p><a href="{link}" target="_blank">Go to review</a></p>
                </div>
                """.format(
                    date=hit.payload['date'],
                    body=hit.payload['body'],
                    score=hit.payload['score'],
                    link=hit.payload['link']
                ),
                unsafe_allow_html=True
            )



if __name__ == "__main__":
    main()
