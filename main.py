import flet as ft
import json
import os
import math

DATA_FILE = "flashcards.json"

default_cards = [
    {"word": "bandwidth", "meaning": "băng thông", "example": "5G needs high bandwidth."},
    {"word": "latency", "meaning": "độ trễ", "example": "Low latency for real-time control."},
    {"word": "throughput", "meaning": "thông lượng", "example": "Throughput measured in Mbps."},
]

def load_cards():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return default_cards

def save_cards(cards):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(cards, f, ensure_ascii=False, indent=2)

# ------------------- MÀN HÌNH FLASHCARD -------------------
def show_flashcards(page: ft.Page, cards, current_index, word_display, meaning_display, example_display,
                    word_input, meaning_input, example_input, update_display_callback):
    # Hàm này sẽ được gọi khi bấm nút "Flashcards"
    # Xóa toàn bộ controls hiện tại trên page
    page.controls.clear()
    
    # Tạo lại giao diện flashcard (giống code cũ)
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
    
    # Nút chuyển sang Playground
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

# ------------------- MÀN HÌNH TELECOM PLAYGROUND -------------------
def show_telecom(page, cards, current_index, word_display, meaning_display, example_display, word_input, meaning_input, example_input, update_display_callback):
    page.controls.clear()
    
    # Các ô nhập liệu
    bandwidth_input = ft.TextField(label="Bandwidth (Hz)", width=300)
    snr_input = ft.TextField(label="SNR (linear ratio)", width=300)
    result_text = ft.Text("", size=18, color=ft.Colors.GREEN_800)
    
    def calculate_shannon(e):
        try:
            B = float(bandwidth_input.value)
            SNR = float(snr_input.value)
            if B <= 0 or SNR <= 0:
                raise ValueError
            C = B * math.log2(1 + SNR)
            result_text.value = f"📡 Channel Capacity = {C:.2f} bps"
        except:
            result_text.value = "❌ Invalid input (positive numbers only)"
        page.update()
    
    # Thêm một vài công thức khác
    def calculate_fspl(e):
        try:
            d = float(distance_input.value)  # km
            f = float(freq_input.value)      # MHz
            fspl = 20 * math.log10(d) + 20 * math.log10(f) + 32.44
            fspl_text.value = f"📡 Free Space Path Loss = {fspl:.2f} dB"
        except:
            fspl_text.value = "❌ Invalid input"
        page.update()
    
    distance_input = ft.TextField(label="Distance (km)", width=300)
    freq_input = ft.TextField(label="Frequency (MHz)", width=300)
    fspl_text = ft.Text("", size=18, color=ft.Colors.BLUE_800)
    
    # Nút quay lại Flashcards
    back_btn = ft.ElevatedButton("← Back to Flashcards", on_click=lambda e: show_flashcards(page, cards, current_index, word_display, meaning_display, example_display, word_input, meaning_input, example_input, update_display_callback))
    
    page.add(
        ft.Column([
            ft.Text("📡 Telecom Engineering Playground", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_900),
            ft.Divider(height=20),
            ft.Text("Shannon-Hartley Theorem", size=18, weight=ft.FontWeight.W_600),
            bandwidth_input,
            snr_input,
            ft.ElevatedButton("Calculate Capacity", on_click=calculate_shannon),
            result_text,
            ft.Divider(height=20),
            ft.Text("Free Space Path Loss", size=18, weight=ft.FontWeight.W_600),
            distance_input,
            freq_input,
            ft.ElevatedButton("Calculate FSPL", on_click=calculate_fspl),
            fspl_text,
            ft.Divider(height=30),
            back_btn
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15)
    )
    page.update()

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
                    word_input, meaning_input, example_input, update_display_callback)

ft.app(target=main)