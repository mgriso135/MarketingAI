import logging
import feedparser
import csv
from bs4 import BeautifulSoup
from config import Config

logger = logging.getLogger(__name__)


class ContentPlanner:
    def __init__(self):
        self.product_updates_file = "product_updates.csv"
        self.rss_feeds = [
            "https://www.leanblog.org/feed/",
            "https://blog.gembaacademy.com/feed/",
            "http://www.aleanjourney.com/feeds/posts/default",
            "https://www.jflinch.com/blog/feed/"  # Add more RSS feeds
        ]

    def get_rss_content(self):
        content = []
        for url in self.rss_feeds:
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries:
                    summary = entry.summary if hasattr(entry, "summary") else ""
                    content.append({"title": entry.title, "summary": summary, "link": entry.link})
            except Exception as e:
                logger.error(f"Error parsing RSS feed {url}: {e}")
        return content

    def get_product_updates(self):
        product_updates = []
        try:
            with open(self.product_updates_file, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    product_updates.append(row)
        except Exception as e:
            logger.error(f"Error reading product updates from CSV: {e}")
        return product_updates


    def plan_content(self):
        rss_content = self.get_rss_content()
        product_updates = self.get_product_updates()

        ideas = []
        for item in rss_content:
            ideas.append(f"Check out this article: {item['title']} - {item['link']} from RSS")
        for update in product_updates:
            ideas.append(f"Our product feature: {update['title']} - {update['description']}")

        logger.info(f"Planned content ideas: {ideas}")
        return ideas