import feedparser

urls = [
    ("https://feeds.feedburner.com/IeeeSpectrumFullText", "IEEE Spectrum"),
    ("https://rss.techxplore.com/rss/telecom", "TechXplore Telecom"),  
    ("https://learningenglish.voanews.com/api/zmpqormvy_t", "VOA Learning English"),
    ("https://www.fiercetelecom.com/rss/xml", "Fierce Telecom"),
    ("https://www.telecompaper.com/rss/all-news", "Telecompaper"),
]

for url, name in urls:
    feed = feedparser.parse(url)
    print(f"\n=== {name} ===")
    print(f"Status: {feed.get('status', 'N/A')}")
    print(f"Bozo: {feed.bozo}")
    print(f"Số entries: {len(feed.entries)}")
    if feed.entries:
        print(f"Bài đầu: {feed.entries[0].get('title', 'N/A')[:60]}")
        