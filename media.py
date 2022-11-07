from typing import List 
from requests import get
from bs4 import BeautifulSoup
import feedparser

MEDIA = {
    "bbc": "http://feeds.bbci.co.uk/news/rss.xml",
    "cnn": "http://rss.cnn.com/rss/edition.rss",
    "abc news": "https://abcnews.go.com/abcnews/topstories",
    "cbs news": "https://www.cbsnews.com/latest/rss/main",
    "fox news": "https://moxie.foxnews.com/google-publisher/latest.xml",
    "new york times": "http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
    "nbc": "http://feeds.nbcnews.com/feeds/topstories",
    "washington post": "http://feeds.washingtonpost.com/rss/business",
    "usa today": "http://rssfeeds.usatoday.com/usatoday-NewsTopStories",
}

def get_all_sources(t=None) -> List[str]:
    return list(MEDIA.keys())

def get_url_for_media(media_source: str) -> str:
    url = MEDIA.get(media_source)
    if not url:
        raise ValueError(f"Invalid media: {media_source}")
    return url

def get_articles(media_source: str):
    url = get_url_for_media(media_source)
    parsed = feedparser.parse(url)
    return {
        entry.get("title"): entry.get("link")
        for entry in parsed.entries
        if entry.get("title") and entry.get("link")
    }

def get_article(url: str):
    html = get(url).content
    soup = BeautifulSoup(html, "html.parser")
    text = " ".join([el.text.strip() for el in soup.find_all(["p", "span", "div"]) if el.text])
    title = soup.title.text
    return {
        "title": title,
        "text": text,
    }
