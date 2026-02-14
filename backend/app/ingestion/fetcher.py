import feedparser
import os
import re
from typing import List, Optional
from datetime import datetime
from app.storage.models import AnalyzeRequest

def clean_html(raw_html: str) -> str:
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext.strip()

class RSSFetcher:
    def __init__(self, feeds_file_path: Optional[str] = None):
        if feeds_file_path:
            self.feeds_file = feeds_file_path
        else:
            # Default path relative to this file: backend/app/ingestion/fetcher.py -> ../../config
            self.feeds_file = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'rss_feeds.txt')

    def get_feeds_list(self) -> List[str]:
        if not os.path.exists(self.feeds_file):
            print(f"RSS feeds file not found at {self.feeds_file}")
            return []

        with open(self.feeds_file, 'r') as file:
            return [line.strip() for line in file if line.strip() and not line.strip().startswith('#')]

    def fetch_all(self) -> List[AnalyzeRequest]:
        feeds = self.get_feeds_list()
        results = []
        
        for feed_url in feeds:
            # Skip invalid URLs
            if not feed_url:
                continue
                
            print(f"Fetching feed: {feed_url}")
            try:
                feed = feedparser.parse(feed_url)
                feed_title = feed.feed.get('title', 'Unknown Source')
                
                for entry in feed.entries:
                    headline = entry.get('title', 'No Title')
                    # Parse date if available, otherwise use now. feedparser usually returns structured time
                    published_parsed = entry.get('published_parsed')
                    if published_parsed:
                        timestamp = datetime(*published_parsed[:6])
                    else:
                        timestamp = datetime.utcnow()
                    
                    description = clean_html(entry.get('description', ''))
                    
                    # Create AnalyzeRequest object
                    request = AnalyzeRequest(
                        headline=headline,
                        source=feed_title,
                        timestamp=timestamp,
                        text=description
                    )
                    results.append(request)
            except Exception as e:
                print(f"Error fetching {feed_url}: {e}")
                
        return results
