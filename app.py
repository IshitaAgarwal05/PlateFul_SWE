import flet as ft
from db.connection import initialize_database
from ui.login_pages import login_page, registration_page, registration_success_page
from ui.onboarding_pages import show_loading
from ui.user.current_order import curr_order


def main(page: ft.Page):
    page.title = "Plateful App"
    page.window_resizable = False  # Disable resizing
    page.window_width = 390  # Mobile width
    page.window_height = 844  # Mobile height
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ft.Colors.ORANGE_800,
            secondary=ft.Colors.RED_600,
            background=ft.Colors.WHITE,
            on_primary=ft.Colors.BLACK,
        )
    )

    # print("AB")
    # Initialize the database (creates tables if not already created)
    try:
        initialize_database()
    except Exception as e:
        print(f"Database initialization error: {e}")

    # print("A")
    # Function to navigate to different views
    def navigate_to(page, view, email=None):
        try:
            page.clean()
            if view == "welcome":
                page.add(show_loading(page, navigate_to))  # Add the returned content
            elif view == "login":
                page.add(login_page(page, navigate_to))
            elif view == "register":
                page.add(registration_page(page, navigate_to))
            elif view == "registration-success":
                page.add(registration_success_page(page, navigate_to))

            elif view == "menu":
                page.add(curr_order(page, email))  # Pass email to curr_order
            elif view == "admin_home":
                from ui.user.home import home_page as admin_home
                page.add(admin_home(page, navigate_to, email))  # Pass email


            elif view == "fs_home":
                from ui.fs.fs_desc import desc
                desc(page, navigate_to, email)
            elif view == "supplier_insights":
                from ui.fs.fs_insights import supplier_insights
                insights_component = supplier_insights(page, email)
                if not isinstance(insights_component, ft.Control):
                    raise ValueError("Invalid component returned")
                page.add(insights_component)


            elif view == "ngo_home":
                from ui.user.home import home_page as ngo_home
                page.add(ngo_home(page, navigate_to, email))  # Pass email


            elif view == "user_home":
                from ui.user.home import home_page as user_home
                page.add(user_home(page, navigate_to, email))  # Pass email


            else:
                ft.Text("🚧 Page not found")  # Prevent `None` issues

            page.update()

        except Exception as e:
            print(f"Navigation error: {e}")
            page.clean()
            page.add(ft.Text(f"Navigation error: {str(e)}", color="red", size=16))
            page.update()

    # Start with the login view
    navigate_to(page, "login")

# print("AC")
ft.app(target=main, view=ft.AppView.FLET_APP_WEB)