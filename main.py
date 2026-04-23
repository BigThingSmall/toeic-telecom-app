import flet as ft
import math

from card_data import load_cards
from flashcard import show_flashcards, update_display_callback
from telecom import show_telecom

# ------------------- HÀM MAIN -------------------
def main(page: ft.Page):
    page.title = "TOEIC 800 + Telecom Engineer"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_maximized = True  
    page.scroll = ft.ScrollMode.AUTO
    
    cards = load_cards()
    # Dùng list để có thể thay đổi current_index từ các hàm (vì nonlocal không hoạt động xuyên hàm)
    current_index = [0]
    
    # Các control dùng chung
    word_display = ft.Text(cards[current_index[0]]["word"], size=40, weight=ft.FontWeight.BOLD)
    meaning_display = ft.Text(cards[current_index[0]]["meaning"], size=24, color=ft.Colors.GREY_700)
    example_display = ft.Text(cards[current_index[0]]["example"], size=16, italic=True, color=ft.Colors.GREY_500)
    word_input = ft.TextField(label="New word", expand=True)
    meaning_input = ft.TextField(label="Meaning", expand=True)
    example_input = ft.TextField(label="Example (optional)", expand=True)
    
    # Khởi tạo màn hình flashcards
    show_flashcards(page, cards, current_index, word_display, meaning_display, example_display,
                    word_input, meaning_input, example_input, update_display_callback, show_telecom)

ft.app(target=main)