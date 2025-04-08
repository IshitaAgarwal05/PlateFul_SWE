import flet as ft
from db.connection import initialize_database
from db.models import get_user_type
from ui.login_pages import login_page, registration_page, registration_success_page
from ui.onboarding_pages import onboarding
# from ui.user.current_order import curr_order


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
    def navigate_to(page, view, email=None, id=None):
        try:
            page.controls.clear()
            page.update()
            page.clean()

            if view == "welcome":
                (onboarding(page, navigate_to)) 
            elif view == "login":
                page.add(login_page(page, navigate_to))
            elif view == "register":
                page.add(registration_page(page, navigate_to))
            elif view == "registration-success":
                page.add(registration_success_page(page, navigate_to))


            elif view == "admin_home":
                from ui.user.home import home_page as admin_home
                page.add(admin_home(page, navigate_to, email))  # Pass email


            elif view == "fs_desc":
                from ui.fs.fs_desc import desc as fs_desc
                fs_desc(page, navigate_to, email)
            elif view == "supplier_insights":
                from ui.fs.fs_insights import supplier_insights
                insights_component = supplier_insights(page, navigate_to, email)
                if not isinstance(insights_component, ft.Control):
                    raise ValueError("Invalid component returned")
                page.add(insights_component)
            elif view == "fs_add_new_food":
                from ui.fs.add_new_food_item import add_new_food
                add_new_food(page, navigate_to, email)


            elif view == "ngo_home":
                from ui.user.home import home_page as ngo_home
                page.add(ngo_home(page, navigate_to, email))  # Pass email
            elif view == "ngo_desc":
                from ui.ngo.ngo_desc import desc as ngo_desc
                page.add(ngo_desc(page, navigate_to, email))
            elif view == "ngo_donation":
                from ui.ngo.ngo_donation import donation_page
                page.add(donation_page(page, navigate_to, email))
            elif view == "ngo_donations_view":
                from ui.ngo.ngo_donations_view import view_donations
                page.add(view_donations(page, navigate_to, email))


            elif view == "user_home":
                from ui.user.home import home_page as user_home
                page.add(user_home(page, navigate_to, email))  # Pass email
            elif view == "user_profile":
                from ui.user.profile import profile
                page.add(profile(page, navigate_to, email))
            elif view == "user_menu_fs":
                from ui.user.user_menu_fs import user_menu_fs
                page.add(user_menu_fs(page, navigate_to, email, id))
            elif view == "user_cart":
                from ui.user.user_cart import cart_page
                page.add(cart_page(page, navigate_to, email, id))


            elif view == "payment_gateway":
                from ui.payment import payment_page
                page.add(payment_page(page, navigate_to, email, amount=None))  # Pass email and amount


            else:
                # Function to handle profile navigation
                def navigate_to_profile(e, email):
                    try:
                        user_type = get_user_type(email)
                        if user_type == "ngo":
                            navigate_to(page, "ngo_desc", email)
                        elif user_type in ["student_verification", "bpl_verification"]:
                            navigate_to(page, "user_profile", email)
                        elif user_type == "food_supplier":
                            navigate_to(page, "fs_profile", email)
                        else:
                            page.snack_bar = ft.SnackBar(
                                ft.Text(f"No profile page available for {user_type} users"),
                                bgcolor=ft.colors.RED
                            )
                            page.snack_bar.open = True
                            page.update()
                    except Exception as e:
                        page.snack_bar = ft.SnackBar(
                            ft.Text(f"Error navigating to profile: {str(e)}"),
                            bgcolor=ft.colors.RED
                        )
                        page.snack_bar.open = True
                        page.update()

                page.add(ft.Column(
                    [
                        ft.Text("🚧 Page content could not be loaded", size=20, color="red"),
                        ft.ElevatedButton(
                            "Go Home",
                            on_click=lambda _: navigate_to_profile(e, email),
                            icon=ft.icons.HOME
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ))

            page.update()

        except Exception as e:
            print(f"Navigation error: {e}")
            page.clean()
            page.add(ft.Text(f"Navigation error: {str(e)}", color="red", size=16))
            page.update()

    # Start with the welcome view
    navigate_to(page, "welcome")

# print("AC")
ft.app(target=main, view=ft.AppView.FLET_APP_WEB)