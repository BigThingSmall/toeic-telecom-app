import flet as ft
import urllib.request
import urllib.parse
import json
from card_data import save_cards


def translate_text(text):
    """Dịch tiếng Anh → tiếng Việt dùng Google Translate (miễn phí)"""
    try:
        text_encoded = urllib.parse.quote(text)
        url = (
            f"https://translate.googleapis.com/translate_a/single"
            f"?client=gtx&sl=en&tl=vi&dt=t&q={text_encoded}"
        )
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            result = json.loads(response.read())
            translated = "".join([item[0] for item in result[0] if item[0]])
            return translated
    except Exception as ex:
        return f"❌ Không dịch được: {ex}"


def show_flashcards(page: ft.Page, cards, current_index, word_display, meaning_display, example_display,
                    word_input, meaning_input, example_input, update_display_callback, show_telecom):
    page.controls.clear()

    # --- Khung dịch ---
    selected_text_field = ft.TextField(
        label="✏️ Nhập hoặc paste từ muốn dịch",
        width=600,
        hint_text="Bôi đen text rồi Ctrl+C, sau đó paste vào đây...",
    )
    translation_result = ft.Text(
        "", size=18, color=ft.Colors.GREEN_800,
        selectable=True,
    )
    translate_btn = ft.ElevatedButton(
        "🌐 Dịch",
        icon=ft.Icons.TRANSLATE,
        on_click=lambda e: do_translate(e, page, selected_text_field, translation_result),
        style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE),
    )

    translate_box = ft.Container(
        content=ft.Column([
            ft.Text("🔍 Tra dịch nhanh", size=16, weight=ft.FontWeight.W_600, color=ft.Colors.BLUE_900),
            ft.Row([selected_text_field, translate_btn], alignment=ft.MainAxisAlignment.CENTER),
            translation_result,
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
        padding=16,
        bgcolor=ft.Colors.BLUE_50,
        border_radius=12,
        border=ft.border.all(1, ft.Colors.BLUE_200),
        width=700,
    )

    # --- Card (bọc trong SelectionArea để bôi đen được) ---
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

    nav_buttons = ft.Row([
        ft.ElevatedButton("◀", on_click=lambda e: prev_click(e, page, cards, current_index, word_display, meaning_display, example_display, update_display_callback),
                          style=ft.ButtonStyle(shape=ft.CircleBorder())),
        ft.ElevatedButton("▶", on_click=lambda e: next_click(e, page, cards, current_index, word_display, meaning_display, example_display, update_display_callback),
                          style=ft.ButtonStyle(shape=ft.CircleBorder())),
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=40)

    add_form = ft.Column([
        word_input, meaning_input, example_input,
        ft.ElevatedButton("Add Flashcard",
                          on_click=lambda e: add_click(e, page, cards, current_index, word_display, meaning_display,
                                                        example_display, word_input, meaning_input, example_input, update_display_callback)),
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10)

    telecom_btn = ft.ElevatedButton(
        "📡 Telecom Playground",
        on_click=lambda e: show_telecom(page, cards, current_index, word_display, meaning_display,
                                         example_display, word_input, meaning_input, example_input, update_display_callback)
    )

    page.add(
        ft.Column([
            ft.Container(height=10),
            ft.Text("📚 TOEIC 800 - Telecom Vocabulary", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
            telecom_btn,
            ft.Divider(height=10),
            card_container,
            nav_buttons,
            ft.Divider(height=10),
            translate_box,       # ← Khung dịch nằm ngay dưới card
            ft.Divider(height=20),
            ft.Text("➕ Add your own word", size=18, weight=ft.FontWeight.W_500),
            add_form,
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)
    )
    page.update()


def do_translate(e, page, selected_text_field, translation_result):
    text = selected_text_field.value.strip()
    if not text:
        translation_result.value = "⚠️ Chưa nhập gì!"
        translation_result.color = ft.Colors.ORANGE_700
    else:
        translation_result.value = "⏳ Đang dịch..."
        translation_result.color = ft.Colors.GREY_500
        page.update()
        result = translate_text(text)
        translation_result.value = f"📖 {result}"
        translation_result.color = ft.Colors.GREEN_800
    page.update()


# Giữ nguyên các hàm cũ bên dưới
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