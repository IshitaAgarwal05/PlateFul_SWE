import flet as ft
import sqlite3
from ui.user.home import wrap_with_nav  # Import the navigation wrapper


def get_user_profile(email):
    conn = sqlite3.connect("plateful.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, contact, email FROM USER WHERE email = ?", (email,))
    result = cursor.fetchone()
    conn.close()
    return {
        "name": result[0],
        "contact": result[1],
        "email": result[2],
    } if result else None


def profile(page: ft.Page, navigate_to, email):
    user_data = get_user_profile(email)
    if not user_data:
        return ft.Text("User not found", color="red")

    def logout(e):
        if hasattr(page, 'user_email'):
            del page.user_email
        navigate_to(page, "login")

    def go_back(e):
        navigate_to(page, "user_home", email)

    profile_column = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        controls=[
            # Back button
            ft.Row([
                ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    on_click=go_back
                ),
                ft.Text("My Profile", size=22, weight="bold")
            ], alignment=ft.MainAxisAlignment.START),

            ft.Divider(),

            # Profile Header
            ft.Column([
                ft.Text(f"Name: {user_data['name']}", size=24, weight="bold"),
                ft.Text(f"Contact: {user_data['contact']}", size=16),
                ft.Text(f"Email: {user_data['email']}", size=16),
            ], spacing=5),

            ft.Divider(),

            # Menu Items
            ft.ListTile(
                title=ft.Text("My Locations"),
                leading=ft.Icon(ft.icons.LOCATION_ON),
                trailing=ft.Icon(ft.icons.CHEVRON_RIGHT),
            ),
            ft.ListTile(
                title=ft.Text("My Promotions"),
                leading=ft.Icon(ft.icons.LOCAL_OFFER),
                trailing=ft.Icon(ft.icons.CHEVRON_RIGHT),
            ),
            ft.ListTile(
                title=ft.Text("Invite Friends"),
                leading=ft.Icon(ft.icons.PERSON_ADD),
                trailing=ft.Icon(ft.icons.CHEVRON_RIGHT),
            ),
            ft.ListTile(
                title=ft.Text("Terms & Services"),
                leading=ft.Icon(ft.icons.SECURITY),
                trailing=ft.Icon(ft.icons.CHEVRON_RIGHT),
            ),
            ft.ListTile(
                title=ft.Text("Help Center"),
                leading=ft.Icon(ft.icons.HELP),
                trailing=ft.Icon(ft.icons.CHEVRON_RIGHT),
            ),

            ft.Divider(),

            # Logout Button
            ft.Container(
                content=ft.ElevatedButton(
                    "Logout",
                    icon=ft.icons.LOGOUT,
                    color=ft.colors.WHITE,
                    bgcolor=ft.colors.RED,
                    on_click=logout,
                    width=200
                ),
                alignment=ft.alignment.center
            )
        ],
        spacing=15
    )

    # White container wrapper
    content = ft.Container(
        content=profile_column,
        padding=20,
        bgcolor=ft.colors.WHITE,
        border_radius=10,
        shadow=ft.BoxShadow(
            blur_radius=8,
            color=ft.colors.with_opacity(0.2, ft.colors.BLACK),
            offset=ft.Offset(0, 4)
        ),
        expand=True
    )

    return ft.Column([
        ft.Container(height=20),
        content
    ], scroll=ft.ScrollMode.AUTO, expand=True)
