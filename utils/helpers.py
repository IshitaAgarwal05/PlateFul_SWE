import flet as ft

def show_toast(page: ft.Page, message: str):
    toast = ft.Text(message, size=16, color="white", weight="bold")
    toast_container = ft.Container(toast, padding=10, bgcolor="green", border_radius=10)
    page.snack_bar = ft.SnackBar(content=toast_container, duration=2000)
    page.snack_bar.open = True
    page.update()
