import pandas as pd
import os
from dotenv import load_dotenv

def obtain_reviews_to_csv():
    file_path = "get_reviews/data/reviews_tripadvisor.csv"
    df = pd.read_csv(file_path)
    return df


