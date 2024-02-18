import streamlit as st
from get_reviews.reviews_tripadvisor import get_reviews_tripadvisor
import datetime


def main():
    st.title('Get TripAdvisor Reviews')
    num_pages = st.number_input('Enter the number of pages:', min_value=1, max_value=10, step=1)

    if st.button('Get reviews'):
        with st.spinner('Downloading reviews...'):
            df = get_reviews_tripadvisor(num_pages)
            st.success('The reviews have been downloaded correctly.')

            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"reviews_tripadvisor_{current_datetime}.csv"

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Reviews CSV",
                data=csv,
                file_name=filename,
                mime="text/csv",
        )


if __name__ == "__main__":
    main()
