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
        if article.find("span", {"class": "size--all-s text--color-grey space--l-1 space--r-2 cept-show-expired-threads hide--toW3"}):
            expired = True
            score =   article.find("span", {"class": "space--h-2 text--b"})
            price =   article.find("span", {"class": "thread-price text--b cept-tp size--all-l size--fromW3-xl text--color-greyShade"})
        else:
            expired =  False
            score =    article.find("span", {"class": "cept-vote-temp vote-temp vote-temp--hot"})
            price =    article.find("span", {"class": "thread-price text--b cept-tp size--all-l size--fromW3-xl"})
        title =         article.find("a", {"class": "cept-tt thread-link linkPlain thread-title--list js-thread-title"})
        datetime =      article.find("span", {"class": "hide--toW3"})
        former_price =  article.find("span", {"class": "mute--text text--lineThrough size--all-l size--fromW3-xl"})
        discount =      article.find("span", {"class": "space--ml-1 size--all-l size--fromW3-xl"})

        article_data = {
            "titre":        title.get("title"),
            "expired":      expired,
            "score":        int(score.text.replace("\xb0", "")),
            "datetime":     datetime.text,
            "price":        price.text,
            "former_price": former_price.text if former_price else None,
            "discount":     discount.text if discount else None
        }
        dataset.append(article_data)

    with open(f"{os.getcwd()}/output/output_data.json", "w") as file:
        file.write(json.dumps(dataset, ensure_ascii=False, indent=4))


make_dataset()
