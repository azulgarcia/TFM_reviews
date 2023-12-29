import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="👋",
)

st.write("## Welcome to review management app! 👋")

st.markdown(
    """
    In this app you can manage Tripadvisor, Google Maps and The Fork reviews for your restaurant.
    ### Get reviews:
    - You can get the reviews you want to manage and get frequent responses for each one.
    - You can also get personalized responses to your reviews.
    ### Review Statistics:
    - Get metrics from your reviews.
    - Analyze the satisfaction and sentiment of your customers.
    - Discover highlights in your customers' opinions.
"""
)