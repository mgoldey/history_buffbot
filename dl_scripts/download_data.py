import os

import requests
from bs4 import BeautifulSoup


def get_article_links(url):
    """Fetches all unique Wikipedia article links from the given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # raises exception for 4xx/5xx errors
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all links on the page
        links = soup.find_all("a")
        article_links = [
            link.get("href")
            for link in links
            if link.get("href") and "/wiki/" in link.get("href")
        ]

        # Filter out links that are not articles (e.g., links to editing pages, categories, etc.)
        article_links = [
            link
            for link in set(article_links)
            if not link.startswith(("/wiki/Special:", "/wiki/Talk:", "/wiki/Category:"))
        ]

        return article_links
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return []


def save_article(article_url, folder="downloaded_articles"):
    """Downloads and saves the content of a Wikipedia article."""
    try:
        response = requests.get(article_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.find("h1").text
        content = soup.find("div", {"class": "mw-parser-output"}).text

        # Create folder if it doesn't exist
        if not os.path.exists(folder):
            os.makedirs(folder)

        # Save article
        filename = f"{title}.txt".replace("/", "_")  # replace to avoid path issues
        filepath = os.path.join(folder, filename)
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)
        print(f"Article '{title}' saved.")

    except requests.RequestException as e:
        print(f"Failed to download article: {e}")


if __name__ == "__main__":
    base_url = "https://en.wikipedia.org"
    start_url = "https://en.wikipedia.org/wiki/Wikipedia:Vital_articles/Level/4/History"

    links = get_article_links(start_url)
    print(f"Found {len(links)} articles to download.")

    for link in links:
        article_url = base_url + link
        save_article(article_url)
