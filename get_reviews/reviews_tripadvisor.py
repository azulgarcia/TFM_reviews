import os
import time
import pandas as pd
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from vector_database.functions_database import connect_to_qdrant, upsert_reviews
from sentimental_analysis.sentiment_analysis_transf import sentimental_analysis_to_df
from sentimental_analysis.sentiment_features import identify_features
from dotenv import load_dotenv
load_dotenv()

URL = os.getenv('URL_ESTABLISHMENT')

def get_reviews_tripadvisor():

    browser = webdriver.Edge()
    browser.get(URL)

    time.sleep(10)

    try:
        cookie_banner = browser.find_element(By.ID, 'onetrust-banner-sdk')
        accept_button = cookie_banner.find_element(By.XPATH, "//button[@id='onetrust-accept-btn-handler']")
        accept_button.click()
    except NoSuchElementException:
        pass

    num_pages = 1

    reviews_data = {"page_number": [], "date": [], "title": [], "body": [], "author": [], "score": [], "link": []}

    page_num = 0


    for _ in range(num_pages):
        reviews = WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'review-container'))
        )
        page_num += 1
        for review in reviews:
            date = review.find_element(By.XPATH, "//div[@class='prw_rup prw_reviews_stay_date_hsx']")
            date = date.text.split(':')[-1].strip()

            title = review.find_element(By.CLASS_NAME, 'noQuotes').text
            body = review.find_element(By.CLASS_NAME, 'partial_entry').text
            post_snippets = review.find_elements(By.XPATH, ".//span[contains(@class, 'postSnippet')]")
            post_snippet_texts = [snippet.get_attribute("textContent") for snippet in post_snippets]

            if post_snippet_texts:
                body = body[:-6]
                body = body + " " + " ".join(post_snippet_texts)

            author = review.find_element(By.CLASS_NAME, 'info_text.pointer_cursor div').text
            rating_element = review.find_element(By.CLASS_NAME, 'ui_bubble_rating').get_attribute('class')
            rating = rating_element[-2]
            link_element = review.find_element(By.CLASS_NAME, 'quote')
            link = link_element.find_element(By.CLASS_NAME, 'title').get_attribute('href')

            reviews_data["page_number"].append(page_num)
            reviews_data["date"].append(date)
            reviews_data["title"].append(title)
            reviews_data["body"].append(body)
            reviews_data["author"].append(author)
            reviews_data["score"].append(rating)
            reviews_data["link"].append(link)

            time.sleep(5)

        next_button = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//a[@class='nav next ui_button primary']"))
        )
        next_button.click()

        time.sleep(10)

    df = pd.DataFrame(reviews_data)
    browser.close()

    df_with_sentiment = sentimental_analysis_to_df(df)

    df_features = df_with_sentiment['body'].apply(identify_features).apply(pd.Series)

    df_reviews_final = pd.concat([df_with_sentiment, df_features], axis=1)

    client = connect_to_qdrant()

    upsert_reviews(client, df_reviews_final)

    return df

print(get_reviews_tripadvisor())