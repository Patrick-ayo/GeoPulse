# rss feed fetcher, supposed to run every two minutes, and the feed list is in ../config
# instruction for feed list:
# each feed on a new line, if want comments put a # like python and maybe perhaps it won't break this

import feedparser
from apscheduler.schedulers.background import BackgroundScheduler
import os
import time
import json
import multiprocessing
import re

def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    return re.sub(cleanr, '', raw_html)

def read_rss_feeds(queue):
    feeds_file = os.path.join(os.path.dirname(__file__), '../config/rss_feeds.txt')
    if not os.path.exists(feeds_file):
        print("RSS feeds file not found.")
        return

    with open(feeds_file, 'r') as file:
        feeds = [line.strip() for line in file if line.strip() and not line.strip().startswith('#')]

    for feed_url in feeds:
        if feed_url:
            print(f"Fetching feed: {feed_url}")
            feed = feedparser.parse(feed_url)
            feed_title = feed.feed.get('title', 'Unknown Source')
            for entry in feed.entries:
                feed_data = {
                    'source_title': feed_title,
                    'item_title': entry.get('title', 'No Title'),
                    'description': clean_html(entry.get('description', 'No Description')),
                    'pubDate': entry.get('published', 'No Publication Date')
                }
                queue.put(feed_data)

scheduler = BackgroundScheduler()
# maybe move this ↓ scheduler to main when it's properly hooked up with multiprocessing
# scheduler.add_job(read_rss_feeds, 'interval', minutes=2)

if __name__ == "__main__":
    print("Starting RSS feed reader...")
    queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=read_rss_feeds, args=(queue,))
    process.start()
    try:
        while True:
            if not queue.empty():
                print("Data for analysis:", queue.get())
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        process.terminate()
