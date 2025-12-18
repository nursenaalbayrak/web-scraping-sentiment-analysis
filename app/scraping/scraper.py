import requests
from bs4 import BeautifulSoup


def scrape_quotes():
    url = "https://quotes.toscrape.com/"
    return []


def get_books():
    url = "https://books.toscrape.com/"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Hata: Kitap listesi çekilemedi: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    books = []

    for book in soup.find_all("article", class_="product_pod"):
        title = book.h3.a["title"]
        link = book.h3.a["href"]

        if "catalogue" not in link:
            full_link = "https://books.toscrape.com/catalogue/" + link
        else:
            full_link = "https://books.toscrape.com/" + link

        # ✅ BOOK COVER IMAGE
        img_tag = book.find("img")
        image_url = None
        if img_tag and img_tag.get("src"):
            image_url = img_tag["src"].replace("../", "")
            image_url = "https://books.toscrape.com/" + image_url

        books.append({
            "title": title,
            "url": full_link,
            "image": image_url
        })

    return books



def get_book_detail(book_url):
    try:
        response = requests.get(book_url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Hata: Kitap detayı çekilemedi ({book_url}): {e}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.find("h1").text

    description_block = soup.find("div", id="product_description")
    if description_block:
        description = description_block.find_next_sibling("p").text
    else:
        description_meta = soup.find("meta", attrs={"name": "description"})
        if description_meta:
            description = description_meta.get("content", "").strip()
        else:
            description = "No description available."

    return {
        "title": title,
        "description": description,
        "url": book_url
    }
