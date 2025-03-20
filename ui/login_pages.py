import flet as ft
from db.models import register_user, login_user

def login_page(page: ft.Page, navigate_to):
    page.title = "Plateful - Login"

    # Email field (replaced username with email)
    email_field = ft.TextField(label="Email", on_change=lambda e: update_login_button_state())
    password_field = ft.TextField(label="Password", password=True, on_change=lambda e: update_login_button_state())

    # Define handle_login before it is referenced
    def handle_login(_):
        if login_user(email_field.value, password_field.value):
            navigate_to("home")
        else:
            # Show "Invalid credentials" message
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Invalid credentials. Try again."),
                action="OK",
                duration=3000  # 3 seconds
            )
            page.snack_bar.open = True
            page.update()

    # Define update_login_button_state
    def update_login_button_state():
        # Enable the button only if both fields are filled
        login_button.disabled = not (email_field.value and password_field.value)
        page.update()

    # Create the login button after handle_login is defined
    login_button = ft.ElevatedButton("Log In", on_click=handle_login, disabled=True)

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Welcome to Plateful", size=24, weight=ft.FontWeight.BOLD),
                email_field,
                password_field,
                ft.Row(
                    controls=[
                        login_button,
                        ft.OutlinedButton("Register", on_click=lambda _: navigate_to("register")),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.center,
        width=400,
        padding=20,
    )




def registration_page(page, navigate_to):
    username_field = ft.TextField(label="Username", on_change=lambda e: update_register_button_state())
    contact_field = ft.TextField(label="Contact Number", on_change=lambda e: update_register_button_state())
    email_field = ft.TextField(label="Email", on_change=lambda e: update_register_button_state())
    user_type_field = ft.Dropdown(
        label="User Type",
        options=[
            ft.dropdown.Option("Admin"),
            ft.dropdown.Option("Employee"),
        ],
        on_change=lambda e: update_register_button_state()
    )
    password_field = ft.TextField(label="Password", password=True, on_change=lambda e: update_register_button_state())

    # Define handle_register before it is referenced
    def handle_register(_):
        if register_user(username_field.value, contact_field.value, email_field.value, user_type_field.value, password_field.value):
            # Show "Registered successfully" message
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Registered successfully!"),
                action="OK",
                duration=3000  # 3 seconds
            )
            page.snack_bar.open = True
            page.update()
            navigate_to("login")  # Navigate to login page after successful registration
        else:
            # Show "Registration failed" message
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Registration failed. Try again!"),
                action="OK",
                duration=3000  # 3 seconds
            )
            page.snack_bar.open = True
            page.update()

    # Define update_register_button_state
    def update_register_button_state():
        # Enable the button only if all fields are filled
        register_button.disabled = not (
            username_field.value and
            contact_field.value and
            email_field.value and
            user_type_field.value and
            password_field.value
        )
        page.update()

    # Create the register button after handle_register is defined
    register_button = ft.ElevatedButton(text="Submit", on_click=handle_register, disabled=True)

    return ft.Container(
        content=ft.Column([
            ft.Text("Register", size=20, weight=ft.FontWeight.BOLD),
            username_field,
            contact_field,
            email_field,
            user_type_field,
            password_field,
            register_button
        ])
    )

def registration_success_page(page, navigate_to):
    page.add(ft.Text("Registration Successful! You can now log in."))
    page.add(ft.ElevatedButton(text="Go to Login", on_click=lambda _: navigate_to("login")))