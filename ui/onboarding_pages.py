import flet as ft
import asyncio

async def show_loading(page):
    page.clean()
    loading_view = ft.Container(
        content=ft.Column(
            [
                ft.Image(src="assets/images/logo.png", width=300, height=300),
                ft.Text("PlateFul hai toh, Pet full hai!", size=20, weight=ft.FontWeight.BOLD),
                ft.ProgressBar(width=300)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.center,
        gradient=ft.LinearGradient(colors=[ft.Colors.RED_800, ft.Colors.ORANGE_500]),
    )

    page.add(loading_view)
    page.update()

    # Simulate a loading delay
    await asyncio.sleep(3)
    show_login_signup(page)

def show_login_signup(page):
    page.clean()
    page.theme = ft.Theme(color_scheme_seed=ft.colors.ORANGE)

    login_card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text("Login", size=30, weight=ft.FontWeight.BOLD),
                    ft.TextField(label="Email", keyboard_type=ft.KeyboardType.EMAIL),
                    ft.TextField(label="Password", password=True, can_reveal_password=True),
                    ft.ElevatedButton("Login", on_click=lambda e: ft.SnackBar(ft.Text("Logged in!")).open)
                ]
            ),
            padding=20,
        )
    )

    signup_card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text("Sign Up", size=30, weight=ft.FontWeight.BOLD),
                    ft.TextField(label="Full Name"),
                    ft.TextField(label="Email", keyboard_type=ft.KeyboardType.EMAIL),
                    ft.TextField(label="Password", password=True, can_reveal_password=True),
                    ft.ElevatedButton("Sign Up", on_click=lambda e: ft.SnackBar(ft.Text("Account created!")).open)
                ]
            ),
            padding=20,
        )
    )

    page.add(
        ft.Row(
            [login_card, signup_card],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )
    page.update()
