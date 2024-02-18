import os
import time
import pandas as pd
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

load_dotenv()

URL = os.getenv('URL_ESTABLISHMENT')

def get_reviews_tripadvisor(num_pages):

    browser = webdriver.Firefox()
    browser.get(URL)

    time.sleep(10)

    try:
        cookie_banner = browser.find_element(By.ID, 'onetrust-banner-sdk')
        accept_button = cookie_banner.find_element(By.XPATH, "//button[@id='onetrust-accept-btn-handler']")
        accept_button.click()
    except NoSuchElementException:
        pass


    reviews_data = {"page_number": [], "date": [], "title": [], "body": [], "author": [], "score": [], "link": []}



    for page in range(1, num_pages+1):
        try:
            read_more_button = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[@class='taLnk ulBlueLinks']"))
            )
            read_more_button.click()
            time.sleep(3)  # Esperar un segundo después de hacer clic en "Ver más"
        except NoSuchElementException:
            pass

        reviews = WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'review-container'))
        )


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

            reviews_data["page_number"].append(page)
            reviews_data["date"].append(date)
            reviews_data["title"].append(title)
            reviews_data["body"].append(body)
            reviews_data["author"].append(author)
            reviews_data["score"].append(rating)
            reviews_data["link"].append(link)

            time.sleep(3)

        next_button = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//a[@class='nav next ui_button primary']"))
        )
        next_button.click()

        time.sleep(10)

    df = pd.DataFrame(reviews_data)
    browser.close()

    return df
