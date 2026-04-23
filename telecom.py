import flet as ft
import math

from flashcard import show_flashcards


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

    back_btn = ft.ElevatedButton(
        "← Back to Flashcards",
        on_click=lambda e: show_flashcards(page, cards, current_index, word_display, meaning_display, example_display, word_input, meaning_input, example_input, update_display_callback, show_telecom)
    )

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
            back_btn,
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15)
    )
    page.update()
