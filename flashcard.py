import flet as ft
from card_data import save_cards


def show_flashcards(page: ft.Page, cards, current_index, word_display, meaning_display, example_display,
                    word_input, meaning_input, example_input, update_display_callback, show_telecom):
    # Hàm này sẽ được gọi khi bấm nút "Flashcards"
    # Xóa toàn bộ controls hiện tại trên page
    page.controls.clear()

    card_container = ft.Container(
        content=ft.Column([
            word_display,
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            meaning_display,
            ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
            example_display,
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=30,
        bgcolor=ft.Colors.WHITE,
        border_radius=20,
        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.GREY_400),
        expand=True,
    )

    nav_buttons = ft.Row([
        ft.ElevatedButton("◀", on_click=lambda e: prev_click(e, page, cards, current_index, word_display, meaning_display, example_display, update_display_callback), style=ft.ButtonStyle(shape=ft.CircleBorder())),
        ft.ElevatedButton("▶", on_click=lambda e: next_click(e, page, cards, current_index, word_display, meaning_display, example_display, update_display_callback), style=ft.ButtonStyle(shape=ft.CircleBorder())),
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=40)

    add_form = ft.Column([
        word_input,
        meaning_input,
        example_input,
        ft.ElevatedButton("Add Flashcard", on_click=lambda e: add_click(e, page, cards, current_index, word_display, meaning_display, example_display, word_input, meaning_input, example_input, update_display_callback)),
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10)

    telecom_btn = ft.ElevatedButton("📡 Telecom Playground", on_click=lambda e: show_telecom(page, cards, current_index, word_display, meaning_display, example_display, word_input, meaning_input, example_input, update_display_callback))

    page.add(
        ft.Column([
            ft.Container(height=10),
            ft.Text("📚 TOEIC 800 - Telecom Vocabulary", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
            telecom_btn,
            ft.Divider(height=10),
            card_container,
            nav_buttons,
            ft.Divider(height=30),
            ft.Text("➕ Add your own word", size=18, weight=ft.FontWeight.W_500),
            add_form,
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)
    )
    page.update()


def prev_click(e, page, cards, current_index, word_display, meaning_display, example_display, update_display_callback):
    current_index[0] = (current_index[0] - 1) % len(cards)
    update_display_callback(current_index[0], cards, word_display, meaning_display, example_display, page)


def next_click(e, page, cards, current_index, word_display, meaning_display, example_display, update_display_callback):
    current_index[0] = (current_index[0] + 1) % len(cards)
    update_display_callback(current_index[0], cards, word_display, meaning_display, example_display, page)


def add_click(e, page, cards, current_index, word_display, meaning_display, example_display, word_input, meaning_input, example_input, update_display_callback):
    new_word = word_input.value.strip()
    new_meaning = meaning_input.value.strip()
    new_example = example_input.value.strip()
    if new_word and new_meaning:
        cards.append({"word": new_word, "meaning": new_meaning, "example": new_example})
        save_cards(cards)
        word_input.value = ""
        meaning_input.value = ""
        example_input.value = ""
        current_index[0] = len(cards) - 1
        update_display_callback(current_index[0], cards, word_display, meaning_display, example_display, page)
        page.snack_bar = ft.SnackBar(ft.Text("Added!"), open=True)
    else:
        page.snack_bar = ft.SnackBar(ft.Text("Please enter word and meaning"), open=True)
    page.update()


def update_display_callback(idx, cards, word_display, meaning_display, example_display, page):
    word_display.value = cards[idx]["word"]
    meaning_display.value = cards[idx]["meaning"]
    example_display.value = cards[idx]["example"]
    page.update()


default_cards = [
    {"word": "bandwidth", "meaning": "băng thông", "example": "5G needs high bandwidth."},
    {"word": "latency", "meaning": "độ trễ", "example": "Low latency for real-time control."},
    {"word": "throughput", "meaning": "thông lượng", "example": "Throughput measured in Mbps."},
]
