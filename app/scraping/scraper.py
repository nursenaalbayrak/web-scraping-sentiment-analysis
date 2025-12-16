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
        
        full_link = "https://books.toscrape.com/" + link

        if "catalogue" not in link:
            full_link = "https://books.toscrape.com/catalogue/" + link

        books.append({
            "title": title,
            "url": full_link
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
        description = soup.find("meta", attrs={"name": "description"})
        if description:
             description = description.get('content', "No description available.").strip()
        else:
            description = "No description available."

    return {
        "title": title,
        "description": description,
        "url": book_url
    }