import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk
import requests
import os

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt_tab')

STOPWORDS = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None
    
def handle_missing_values(df):
    df.dropna(subset=['title', 'content'], inplace=True)
    df['link'].fillna('', inplace=True)
    return df

def normalize_text(text):
    if not isinstance(text, str): 
        return ''
    
    text = text.lower()

    text = re.sub(r"http\S+|www.\S+", "", text)

    text = re.sub(r"[^a-zA-Z\s]", "", text)

    tokens = word_tokenize(text)

    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in STOPWORDS]

    return " ".join(tokens)

def validate_links(df):
    def is_valid_url(url):
        try:
            response = requests.head(url, timeout=5)
            return response.status_code == 200
        except:
            return False
    
    df['is_valid_link'] = df['link'].apply(lambda x: is_valid_url(x) if x else False)
    return df

def clean_data(df):
    df['cleaned_title'] = df['title'].apply(normalize_text)
    df['cleaned_content'] = df['content'].apply(normalize_text)

    df = validate_links(df)
    
    return df
def save_cleaned_data(df, output_file):
    try:
        df.to_csv(output_file, index=False)
        print(f"Cleaned data saved to {output_file}")
    except Exception as e:
        print(f"Error saving cleaned data: {e}")

input_file = os.path.abspath("../data/outbreak_data_1.csv")
output_file = "../data/cleaned_data.csv"

df = load_data(input_file)
if df is None:
        exit()

df = handle_missing_values(df)

df = clean_data(df)

save_cleaned_data(df, output_file)
   
