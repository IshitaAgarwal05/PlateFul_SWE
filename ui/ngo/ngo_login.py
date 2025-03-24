import flet as ft

def main(page: ft.Page):
    page.title = "Plateful Sign Up"
    page.bgcolor = "#F8F8F8"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Background Image Section
    background = ft.Container(
        height=250,
        content=ft.Column(
            [
                ft.Image(
                    src="https://your-image-url.com",  # Replace with your hosted image URL
                    fit=ft.ImageFit.COVER,
                    width=400,
                    height=250,
                ),
                ft.Text(
                    "PLATEFUL",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color="white",
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )

    # Sign Up Form
    signup_section = ft.Container(
        padding=20,
        bgcolor=ft.LinearGradient(
            colors=["#D84315", "#FF9800"],  # Gradient color matching the design
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center
        ),
        border_radius=ft.border_radius.only(top_left=30, top_right=30),
        content=ft.Column(
            [
                ft.Text("Sign Up", size=20, weight=ft.FontWeight.BOLD, color="white"),

                # Username Input
                ft.TextField(
                    label="Username",
                    prefix_icon=ft.icons.PERSON,
                    bgcolor="white",
                    border_radius=8,
                    width=300,
                ),

                # Password Input
                ft.TextField(
                    label="Password",
                    prefix_icon=ft.icons.KEY,
                    bgcolor="white",
                    password=True,
                    border_radius=8,
                    width=300,
                ),

                # OR Divider
                ft.Row(
                    [
                        ft.Container(width=100, content=ft.Divider(color="white")),
                        ft.Text("OR", color="white"),
                        ft.Container(width=100, content=ft.Divider(color="white")),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),

                ft.Text("Register Via", size=14, weight=ft.FontWeight.BOLD, color="white"),

                # Social Media Buttons
                ft.ElevatedButton(
                    text="Sign In with Gmail",
                    icon=ft.icons.EMAIL,
                    bgcolor="white",
                    color="black",
                    width=300,
                ),

                ft.Row(
                    [
                        ft.ElevatedButton(
                            text="Facebook",
                            icon=ft.icons.FACEBOOK,
                            bgcolor="white",
                            color="black",
                            width=140,
                        ),
                        ft.ElevatedButton(
                            text="Google",
                            icon=ft.icons.GOOGLE,
                            bgcolor="white",
                            color="black",
                            width=140,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),

                # Footer
                ft.Text(
                    "By continuing, you agree to our Terms of Service, Privacy Policy, and Content Policy.",
                    size=10,
                    color="white",
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        ),
    )

    # Full Page Layout
    page.add(
        ft.Column(
            [background, signup_section],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

ft.app(target=main)
