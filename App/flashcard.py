import flet as ft
import urllib.request
import urllib.parse
import json
from card_data import save_cards


def translate_text(text):
    try:
        text = text[:300]
        text_encoded = urllib.parse.quote(text)
        url = (
            f"https://translate.googleapis.com/translate_a/single"
            f"?client=gtx&sl=auto&tl=vi&dt=t&q={text_encoded}"
        )
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            result = json.loads(response.read())
            return "".join([item[0] for item in result[0] if item[0]])
    except Exception as ex:
        return f"❌ Lỗi: {ex}"


def show_flashcards(page: ft.Page, cards, current_index, word_display, meaning_display, example_display,
                    word_input, meaning_input, example_input, update_display_callback, show_telecom):
    page.controls.clear()

    # Ô nhập ẩn + kết quả dịch - gọn nhẹ
    quick_input = ft.TextField(
        hint_text="Bôi đen → Ctrl+C → Ctrl+V vào đây → Enter",
        border_radius=8,
        expand=True,
        on_submit=lambda e: do_translate(e),  # Bấm Enter để dịch
        dense=True,
    )
    result_text = ft.Text("", size=15, color=ft.Colors.GREEN_800, selectable=True, visible=False)

    def do_translate(e):
        text = quick_input.value.strip()
        if not text:
            return
        result_text.value = "⏳..."
        result_text.visible = True
        page.update()
        result_text.value = translate_text(text)
        quick_input.value = ""
        page.update()

    mini_translate_bar = ft.Container(
        content=ft.Row([
            ft.Text("🌐", size=16),
            quick_input,
            ft.IconButton(
                icon=ft.Icons.SEND_ROUNDED,
                icon_color=ft.Colors.BLUE_600,
                tooltip="Dịch (hoặc bấm Enter)",
                on_click=do_translate,
            ),
        ], spacing=6, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        padding=ft.padding.symmetric(horizontal=12, vertical=6),
        bgcolor=ft.Colors.WHITE,
        border_radius=10,
        border=ft.border.all(1, ft.Colors.BLUE_100),
        expand=True,
    )

    card_container = ft.Container(
        content=ft.SelectionArea(
            content=ft.Column([
                word_display,
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                meaning_display,
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                example_display,
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        ),
        padding=30,
        bgcolor=ft.Colors.WHITE,
        border_radius=20,
        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.GREY_400),
        expand=True,
    )

    def go_prev(e):
        result_text.visible = False
        quick_input.value = ""
        prev_click(e, page, cards, current_index, word_display, meaning_display,
                   example_display, update_display_callback)

    def go_next(e):
        result_text.visible = False
        quick_input.value = ""
        next_click(e, page, cards, current_index, word_display, meaning_display,
                   example_display, update_display_callback)

    nav_buttons = ft.Row([
        ft.ElevatedButton("◀", on_click=go_prev, style=ft.ButtonStyle(shape=ft.CircleBorder())),
        ft.ElevatedButton("▶", on_click=go_next, style=ft.ButtonStyle(shape=ft.CircleBorder())),
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=40)

    add_form = ft.Column([
        word_input, meaning_input, example_input,
        ft.ElevatedButton("Add Flashcard",
                          on_click=lambda e: add_click(e, page, cards, current_index, word_display,
                                                        meaning_display, example_display, word_input,
                                                        meaning_input, example_input, update_display_callback)),
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10)

    telecom_btn = ft.ElevatedButton(
        "📡 Telecom Playground",
        on_click=lambda e: show_telecom(page, cards, current_index, word_display, meaning_display,
                                         example_display, word_input, meaning_input, example_input,
                                         update_display_callback),
    )

    page.add(
        ft.Column([
            ft.Container(height=10),
            ft.Text("📚 TOEIC 800 - Telecom Vocabulary", size=24,
                    weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
            telecom_btn,
            ft.Divider(height=10),
            card_container,
            # Thanh dịch gọn ngay dưới card
            mini_translate_bar,
            result_text,
            nav_buttons,
            ft.Divider(height=20),
            ft.Text("➕ Add your own word", size=18, weight=ft.FontWeight.W_500),
            add_form,
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10)
    )
    page.update()


def prev_click(e, page, cards, current_index, word_display, meaning_display, example_display, update_display_callback):
    current_index[0] = (current_index[0] - 1) % len(cards)
    update_display_callback(current_index[0], cards, word_display, meaning_display, example_display, page)


def next_click(e, page, cards, current_index, word_display, meaning_display, example_display, update_display_callback):
    current_index[0] = (current_index[0] + 1) % len(cards)
    update_display_callback(current_index[0], cards, word_display, meaning_display, example_display, page)


def add_click(e, page, cards, current_index, word_display, meaning_display, example_display,
              word_input, meaning_input, example_input, update_display_callback):
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