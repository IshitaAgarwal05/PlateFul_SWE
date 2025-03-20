import flet as ft
from db.connection import initialize_database
from ui.login_pages import login_page, registration_page, registration_success_page
from ui.home import home_page

def main(page: ft.Page):
    page.title = "Plateful App"
    page.window_resizable = False
    page.window_width = 390
    page.window_height = 844
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ft.Colors.ORANGE_800,
            secondary=ft.Colors.RED_600,
            background=ft.Colors.WHITE,
            on_primary=ft.Colors.BLACK,
        )
    )

    # Initialize the database
    try:
        initialize_database()
    except Exception as e:
        print(f"Database initialization error: {e}")

    # ✅ Route handling function
    def route_change(route):
        page.views.clear()

        if page.route == "/login":
            page.views.append(ft.View("/login", [login_page(page, lambda v: page.go(v))]))

        elif page.route == "/register":
            page.views.append(ft.View("/register", [registration_page(page, lambda v: page.go(v))]))

        elif page.route == "/registration-success":
            page.views.append(ft.View("/registration-success", [registration_success_page(page, lambda v: page.go(v))]))

        elif page.route == "/home":
            page.views.append(ft.View("/home", [home_page(page, lambda v: page.go(v))]))

        page.update()

    # ✅ Route handling event listener
    page.on_route_change = route_change

    # ✅ Open app with login page
    page.go("/login")

ft.app(target=main, view=ft.AppView.FLET_APP_WEB)
