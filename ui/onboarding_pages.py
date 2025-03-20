import flet as ft
import asyncio

# def main(page: ft.Page):
#     page.title = "PlateFul"
#     page.window_width = 390  # Mobile width
#     page.window_height = 800  # Mobile height
#     page.theme = ft.Theme(font_family="Roboto")
#     page.padding = 10
#     page.scroll = ft.ScrollMode.AUTO
#
#     # Function to handle route changes
#     def route_change(route):
#         page.views.clear()
#         if page.route == "/":
#             page.views.append(home_page(page))
#         elif page.route == "/next":
#             page.views.append(next_page(page))
#         page.update()
#
#     # Initial Route Setup
#     page.on_route_change = route_change
#     page.go("/")  # Start with the home screen
#
# # First Screen with Background Image
# def home_page(page):
#     return ft.View(
#         route="/",
#         controls=[
#             ft.Container(
#                 image_src="assets/images/1_white.png",  # Background Image URL
#                 expand=True,
#                 content=ft.Column(
#                     controls=[
#                         ft.Text("PlateFul hai toh,", size=24, weight=ft.FontWeight.BOLD, color="white"),
#                         ft.Text("Pet full hai!", size=24, weight=ft.FontWeight.BOLD, color="white"),
#                         ft.Text("Version 1.0", size=14, italic=True, color="white"),
#                         ft.ElevatedButton("Continue", on_click=lambda _: page.go("/next")),
#                     ],
#                     alignment=ft.MainAxisAlignment.CENTER,
#                     horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#                 ),
#                 alignment=ft.alignment.center,
#                 padding=20,
#             )
#         ],
#     )
#
# # Second Screen
# def next_page(page):
#     return ft.View(
#         route="/next",
#         controls=[
#             ft.Container(
#                 content=ft.Text("Welcome to Page X", size=20, weight=ft.FontWeight.BOLD),
#                 padding=10,
#                 alignment=ft.alignment.center,
#             ),
#             ft.Column(
#                 controls=[
#                     ft.TextField(label="Enter your name"),
#                     ft.ElevatedButton("Submit", on_click=lambda _: print("Submitted")),
#                     ft.Image(src="assets/images/bg_1.png", width=100, height=100),
#                 ],
#                 spacing=20,
#                 alignment=ft.MainAxisAlignment.CENTER,
#             ),
#             ft.BottomAppBar(
#                 content=ft.Row(
#                     controls=[
#                         ft.IconButton(ft.icons.HOME, on_click=lambda _: page.go("/")),
#                         ft.IconButton(ft.icons.SEARCH, on_click=lambda _: page.go("/search")),
#                         ft.IconButton(ft.icons.PERSON, on_click=lambda _: page.go("/profile")),
#                     ],
#                     alignment=ft.MainAxisAlignment.SPACE_AROUND,
#                 )
#             ),
#         ],
#     )
#
# ft.app(target=main)





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
