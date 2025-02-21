import flet as ft

def main(page: ft.Page):
    page.title = "Plateful Sign Up"
    page.bgcolor = "#F8F8F8"
    page.window_width = 390  # Mobile width
    page.window_height = 800  # Mobile height
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Logo and Title
    logo = ft.Text("PLATEFUL", size=28, weight=ft.FontWeight.BOLD, color="#333")

    # Username & Password Fields
    username = ft.TextField(label="Username", prefix_icon=ft.icons.PERSON, width=300)
    password = ft.TextField(label="Password", password=True, prefix_icon=ft.icons.LOCK, width=300)

    # Sign Up Button
    signup_button = ft.ElevatedButton(
        text="Sign Up", 
        bgcolor="#FF5722", 
        color="white",
        width=300,
        on_click=lambda _: print("Sign Up Clicked")
    )

    # Divider
    divider = ft.Row(
        [
            ft.Container(width=100, content=ft.Divider()),
            ft.Text("OR"),
            ft.Container(width=100, content=ft.Divider())
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    # Social Login Buttons
    google_button = ft.ElevatedButton(
        text="Sign in with Google",
        icon=ft.Image(src="https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg"),
        bgcolor="white",
        color="black",
        width=300,
        on_click=lambda _: print("Google Sign-In Clicked")
    )

    email_button = ft.ElevatedButton(
        text="Sign in with Email",
        icon=ft.icons.EMAIL,
        bgcolor="white",
        color="black",
        width=300,
        on_click=lambda _: print("Email Sign-In Clicked")
    )

    # Terms of Service and Privacy Policy Buttons
    tos_button = ft.TextButton(
        "Terms of Service", on_click=lambda _: page.go("/TOS")
    )
    privacy_button = ft.TextButton(
        "Privacy Policy", on_click=lambda _: page.go("/Privacy_policy")
    )

    # Footer with Buttons
    footer = ft.Row(
        [
            ft.Text("By continuing, you agree to our "),
            tos_button,
            ft.Text(" & "),
            privacy_button,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # Page Layout
    page.add(
        ft.Container(  # Wrap in a Container to allow vertical alignment
            content=ft.Column(
                [
                    logo,
                    username,
                    password,
                    signup_button,
                    divider,
                    google_button,
                    email_button,
                    footer
                ],
                alignment=ft.MainAxisAlignment.END,  # Pushes everything down
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10
            ),
            expand=True  # Expands container to full page height
        )
    )


def TOS(page: ft.Page):
    return ft.View(
        route="/",
        controls=[
            ft.Container(
                image_src="assets/images/1_white.png",  # Background Image URL
                expand=True,
                content=ft.Column(
                    controls=[
                        ft.Text("PlateFul hai toh,", size=24, weight=ft.FontWeight.BOLD, color="white"),
                        ft.Text("Pet full hai!", size=24, weight=ft.FontWeight.BOLD, color="white"),
                        ft.Text("Version 1.0", size=14, italic=True, color="white"),
                        ft.ElevatedButton("Continue", on_click=lambda _: page.go("/next")),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                alignment=ft.alignment.center,
                padding=20,
            )
        ],
    )

def Privacy_policy(page: ft.Page):
    return ft.View(
        route="/",
        controls=[
            ft.Container(
                image_src="assets/images/1_white.png",  # Background Image URL
                expand=True,
                content=ft.Column(
                    controls=[
                        ft.Text("PlateFul hai toh,", size=24, weight=ft.FontWeight.BOLD, color="white"),
                        ft.Text("Pet full hai!", size=24, weight=ft.FontWeight.BOLD, color="white"),
                        ft.Text("Version 1.0", size=14, italic=True, color="white"),
                        ft.ElevatedButton("Continue", on_click=lambda _: page.go("/next")),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                alignment=ft.alignment.center,
                padding=20,
            )
        ],
    )


ft.app(target=main)