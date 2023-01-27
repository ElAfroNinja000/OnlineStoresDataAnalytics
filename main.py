import json
import os

import requests
from bs4 import BeautifulSoup

URL     = "https://www.dealabs.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
}


def get_raw_data():
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup.find("div", {"class": "cept-event-deals js-threadList listLayout-main cept-personalization-default cept-picking-method-manual_picks"})


def make_dataset():
    dataset = []
    raw_data = get_raw_data()
    articles = raw_data.find_all("article")
    for article in articles:
        article_data = {"titre": article.find("a", {"class": "cept-tt thread-link linkPlain thread-title--list js-thread-title"}).get("title")}
        dataset.append(article_data)

    with open(f"{os.getcwd()}/output/output_data.json", "w") as file:
        file.write(json.dumps(dataset, ensure_ascii=False, indent=4))


make_dataset()
