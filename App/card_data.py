import json
import os

DATA_FILE = "flashcards.json"

def load_cards():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return default_cards


def save_cards(cards):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(cards, f, ensure_ascii=False, indent=2)


default_cards = [
    {"word": "bandwidth", "meaning": "băng thông", "example": "5G needs high bandwidth."},
    {"word": "latency", "meaning": "độ trễ", "example": "Low latency for real-time control."},
    {"word": "throughput", "meaning": "thông lượng", "example": "Throughput measured in Mbps."},
]
