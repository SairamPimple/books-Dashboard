import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
from pathlib import Path

BASE_URL = 'http://books.toscrape.com/catalogue/page-{}.html'

def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.content, 'html.parser')

def scrape_books():
    books = []
    
    for page_num in range(1, 51):  # 50 pages, 20 books each
        print(f"Scraping page {page_num}...")
        soup = get_soup(BASE_URL.format(page_num))

        for article in soup.select('article.product_pod'):
            title = article.h3.a['title']
            price = article.select_one('.price_color').text[2:]  # Remove '£'
            stock = article.select_one('.instock.availability').text.strip()
            rating = article.p['class'][1]  # e.g., 'Three', 'Five'
            relative_link = article.h3.a['href']
            link = urljoin(BASE_URL.format(page_num), relative_link)

            books.append({
                'Title': title,
                'Price': float(price),
                'Stock': stock,
                'Rating': rating,
                'URL': link
            })

    return pd.DataFrame(books)

if __name__ == '__main__':
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    DATA_DIR = PROJECT_ROOT / 'data'
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    df = scrape_books()
    df.to_csv(DATA_DIR / 'books_data.csv', index=False)

    print("✅ Scraping completed. 1000 books saved to data/books_data.csv")


# other method (run in books/scraper dir)
# import os
# if __name__ == '__main__':
#     os.makedirs('../data', exist_ok=True)
#     df = scrape_books()
#     df.to_csv('../data/books_data.csv', index=False)
#     print("✅ Scraping completed. 1000 books saved to data/books_data.csv")