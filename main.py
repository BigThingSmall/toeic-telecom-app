import flet as ft
import requests
import json
import math

from card_data import load_cards, save_cards
from flashcard import show_flashcards, update_display_callback
from telecom import show_telecom

GITHUB_RAW_URL = "https://raw.githubusercontent.com/BigThingSmall/toeic-telecom-app/main/flashcards.json"

def load_cards_from_github():
    try:
        response = requests.get(GITHUB_RAW_URL, timeout=5)
        response.raise_for_status()
        cards = response.json()
        save_cards(cards)  # Lưu local để dùng offline
        print(f"✅ Đã tải {len(cards)} thẻ từ GitHub")
        return cards
    except Exception as ex:
        print(f"⚠️ Không tải được từ GitHub: {ex} → dùng file local")
        return load_cards()  # Fallback về local nếu mất mạng

def main(page: ft.Page):
    page.title = "TOEIC 800 + Telecom Engineer"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_maximized = True
    page.scroll = ft.ScrollMode.AUTO

    cards = load_cards_from_github()  # ← Thay load_cards() bằng hàm này
    current_index = [0]

    word_display = ft.Text(cards[current_index[0]]["word"], size=40, weight=ft.FontWeight.BOLD)
    meaning_display = ft.Text(cards[current_index[0]]["meaning"], size=24, color=ft.Colors.GREY_700)
    example_display = ft.Text(cards[current_index[0]]["example"], size=16, italic=True, color=ft.Colors.GREY_500)
    word_input = ft.TextField(label="New word", expand=True)
    meaning_input = ft.TextField(label="Meaning", expand=True)
    example_input = ft.TextField(label="Example (optional)", expand=True)

    show_flashcards(page, cards, current_index, word_display, meaning_display, example_display,
                    word_input, meaning_input, example_input, update_display_callback, show_telecom)

ft.app(target=main)