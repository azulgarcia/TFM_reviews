import pandas as pd
import streamlit as st
from vector_database.functions_database import get_all_reviews, connect_to_qdrant
import altair as alt
from datetime import datetime
def main():
    st.markdown("""
        TODO
        - chek dates
    """)

    qdrant_client= connect_to_qdrant()
    collection_name = "reviews"
    df_reviews = get_all_reviews(qdrant_client, collection_name)

    months = {
        "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6,
        "julio": 7, "agosto": 8, "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
    }

    def convertir_a_fecha(date_str):
        month, year = date_str.split(" de ")
        return datetime(int(year), months[month.lower()], 1)

    df_reviews['date'] = pd.to_datetime(df_reviews['date'].apply(convertir_a_fecha))

    min_date = min(df_reviews['date'])
    max_date = max(df_reviews['date'])

    coldate1, coldate2 = st.columns(2)
    with coldate1:
        selected_start_date = st.date_input("Select start date", min_value=min_date, max_value=max_date,
                                        value=min_date)
    with coldate2:
        selected_end_date = st.date_input("Select end date", min_value=selected_start_date, max_value=max_date,
                                      value=max_date)

    selected_start_date = pd.Timestamp(selected_start_date)
    selected_end_date = pd.Timestamp(selected_end_date)

    filtered_reviews = df_reviews[
        (df_reviews['date'] >= selected_start_date) & (df_reviews['date'] <= selected_end_date)
        ]

    st.markdown("## Review analysis")

    positive_reviews = filtered_reviews[(filtered_reviews['score'] == 4) | (filtered_reviews['score'] == 5)].shape[0]

    negative_reviews = filtered_reviews[(filtered_reviews['score'] == 1) | (filtered_reviews['score'] == 2)].shape[0]

    total_reviews = filtered_reviews.shape[0]

    average_score = (positive_reviews - negative_reviews) / total_reviews * 100

    table_data = f"""
    <table style="width:50%; text-align:center; font-size: 12px;">
      <tr>
        <th>Total reviews</th>
        <th>Positive</th>
        <th>Negative</th>
      </tr>
      <tr>
        <td>{total_reviews}</td>
        <td>{positive_reviews}</td>
        <td>{negative_reviews}</td>
      </tr>
    </table>
    """

    st.markdown(table_data, unsafe_allow_html=True)
    st.markdown("")
    st.success(f"###### Customer satisfaction: {average_score:.2f}%")


    # score graph
    #st.subheader("Cantidad de Reseñas por Score")
    grouped_score = filtered_reviews.groupby('score').size().reset_index(name='count')

    score_range = range(1, 6)
    data = {'score': [f'⭐️ {i}' for i in score_range],
            'count': [grouped_score.loc[grouped_score['score'] == i, 'count'].values[0] if i in grouped_score[
                'score'].values else 0 for i in score_range]}

    df = pd.DataFrame(data)

    bars = alt.Chart(df).mark_bar(color='#FFD700').encode(
        y=alt.Y('score:N', axis=alt.Axis(title=None), sort=list(data['score'])),
        x=alt.X('count:Q', axis=alt.Axis(title=None, labels=False, ticks=False)),
    )

    chart_1 = bars.configure_view(strokeOpacity=0).configure_axis(grid=False)

    #st.altair_chart(chart, use_container_width=True)

    emoji_mapping = {'1 stars': '😠', '2 stars': '😟', '3 stars': '😐', '4 stars': '😊', '5 stars': '😃'}

    grouped_sentiment = filtered_reviews.groupby('sentiment_label').size().reset_index(name='count')

    sentiment_labels = ['1 stars', '2 stars', '3 stars', '4 stars', '5 stars']
    data = {'sentiment_label': [emoji_mapping.get(label, label) for label in sentiment_labels],
            'count': [
                grouped_sentiment.loc[grouped_sentiment['sentiment_label'] == label, 'count'].values[0] if label in
                                                                                                           grouped_sentiment[
                                                                                                               'sentiment_label'].values else 0
                for label in sentiment_labels]}

    df = pd.DataFrame(data)

    bars = alt.Chart(df).mark_bar(color='#FFD700').encode(
        y=alt.Y('sentiment_label:N', axis=alt.Axis(title=None), sort=list(df['sentiment_label'])),
        x=alt.X('count:Q', axis=alt.Axis(title=None, labels=False, ticks=False)),
        tooltip=['sentiment_label', 'count']
    )

    chart_2 = bars.configure_view(strokeOpacity=0).configure_axis(grid=False)

    #st.subheader("Cantidad de Reseñas por Sentimiento")
    #st.altair_chart(chart, use_container_width=True)

    col1, col2 = st.columns(2)
    #col1.subheader("Cantidad de Reseñas por Score")
    col1.markdown("#### Reviews by score")
    col1.altair_chart(chart_1, use_container_width=True)

    col2.markdown("#### Reviews by sentiment")
    col2.altair_chart(chart_2, use_container_width=True)

    df_date = filtered_reviews.groupby('date').size().reset_index(name='count')

    chart = alt.Chart(df_date).mark_bar().encode(
        x='date:T',
        y='count:Q'
    ).properties(
        title='Historical reviews'
    )

    st.altair_chart(chart, use_container_width=True)


if __name__ == "__main__":
    main()
