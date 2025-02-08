from utils import util as utils
import os
from dotenv import load_dotenv
import time

load_dotenv()


url = os.getenv("WEB_URL_TWO")
baseUrl = os.getenv("BASE_URL_TWO")

soup = utils.fetch_and_parse(url)

def scrap_data_from_website(soup):
    print("Extracting data...")
    time.sleep(1)
    raw_data = []
    for item in soup.find_all('div', class_='col-sm-10'):
     
        link = item.find('a')
        titleTag = item.find('h3')
        if titleTag and link:
            title = titleTag .get_text(strip=True)
            href = link["href"]
            full_url = baseUrl + href

            content = fetch_content_from_link(full_url)
            if content:
                raw_data.append({"title": title, "link": href, "content": content})
            else:
                print(f"Skipping article with link {full_url} due to missing content.")
        else:
            print(f"Could not find title or link on {url}")
    return raw_data

def fetch_content_from_link(link):
    print(f"Fetching content from {link}...")
    time.sleep(2)
    soup = utils.fetch_and_parse(link)

    if soup == None:
        return None
    else:
        content_div = soup.find('div', class_='col-sm-7')  
                
        if content_div:
            return content_div.get_text(strip=True)
        else:
            print(f"Could not find content on {url}")
            return None

data = scrap_data_from_website(soup)

output_file = 'data/outbreak_data_1.csv'
fieldnames = ["title", "link", "content"]
utils.save_to_csv(data, output_file, fieldnames)