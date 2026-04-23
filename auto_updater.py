import feedparser
import re
from card_data import load_cards, save_cards

RSS_SOURCES = [
    ("https://feeds.feedburner.com/IeeeSpectrumFullText", "IEEE Spectrum"),
    ("https://www.fiercetelecom.com/rss/xml", "Fierce Telecom"),
    ("https://techxplore.com/rss-feed/telecom-news/", "TechXplore Telecom"),
]

def strip_html(text):
    return re.sub(r'<[^>]+>', '', text).strip()

def fetch_all_rss():
    existing_cards = load_cards()
    existing_words = {card["word"] for card in existing_cards}

    new_cards = []

    for url, source_name in RSS_SOURCES:
        try:
            feed = feedparser.parse(url)

            if feed.bozo and len(feed.entries) == 0:
                print(f"[{source_name}] ❌ Không truy cập được hoặc feed lỗi.")
                continue

            entries = feed.entries[:3]

            for entry in entries:
                title = strip_html(entry.get("title", "")).strip()[:50]
                summary = strip_html(entry.get("summary", "")).strip()[:200]

                if not title or title in existing_words:
                    continue

                new_cards.append({
                    "word": title,
                    "meaning": source_name,
                    "example": summary,
                })
                existing_words.add(title)

            print(f"[{source_name}] ✅ Đã xử lý {len(entries)} bài.")

        except Exception as ex:
            print(f"[{source_name}] ❌ Lỗi: {ex}")

    if new_cards:
        updated_cards = new_cards + existing_cards
        save_cards(updated_cards)
        print(f"\n✅ Đã thêm {len(new_cards)} thẻ mới vào flashcards.json")
    else:
        print("\nℹ️ Không có thẻ mới nào được thêm.")

if __name__ == "__main__":
    fetch_all_rss()