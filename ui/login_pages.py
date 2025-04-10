import flet as ft
import sqlite3
from db.models import register_user, login_user
import asyncio


def login_page(page: ft.Page, navigate_to):
    page.title = "Plateful - Login"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#f5f5f5"

    # 🖼️ Background Image (full screen behind all content)
    background_image = ft.Image(
        src="/assets/images/elements/general/bg_1.png",
        fit=ft.ImageFit.COVER,
        width=page.width,
        height=page.height,
        expand=True,
        opacity=0.8
    )

    # 📧 Login fields
    email_field = ft.TextField(label="Email", on_change=lambda e: update_login_button_state())
    password_field = ft.TextField(label="Password", password=True, on_change=lambda e: update_login_button_state())

    def get_user_role(email):
        conn = sqlite3.connect("plateful.db")
        cursor = conn.cursor()

        role_queries = {
            "admin": 'SELECT email FROM admin WHERE email = ?',
            "food_supplier": 'SELECT email FROM food_supplier WHERE email = ?',
            "ngo": 'SELECT email FROM ngo WHERE email = ?',
            "student_verification": 'SELECT email FROM student_verification WHERE email = ?',
            "bpl_verification": 'SELECT email FROM bpl_verification WHERE email = ?'
        }

        for role, query in role_queries.items():
            cursor.execute(query, (email,))
            if cursor.fetchone():
                conn.close()
                return role

        conn.close()
        return None

    def handle_login(_):
        email = email_field.value
        password = password_field.value

        if not login_user(email, password):
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Invalid credentials. Try again.", color="black"),
                bgcolor="red",
                action="OK",
                duration=5000
            )
            page.snack_bar.open = True
            page.update()
            return

        user_role = get_user_role(email)

        if user_role == "admin":
            navigate_to(page, "admin_home", email)
        elif user_role == "food_supplier":
            navigate_to(page, "fs_desc", email)
        elif user_role == "ngo":
            navigate_to(page, "ngo_desc", email)
        elif user_role in ["student_verification", "bpl_verification"]:
            navigate_to(page, "user_home", email)
        else:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("User role not recognized.", color="black"),
                bgcolor="red",
                action="OK",
                duration=5000
            )
            page.snack_bar.open = True
            page.update()

    def update_login_button_state():
        login_button.disabled = not (email_field.value and password_field.value)
        page.update()

    login_button = ft.ElevatedButton("Log In", on_click=handle_login, disabled=True)

    # 🧾 Foreground Login Form
    login_form = ft.Container(
        padding=30,
        border_radius=20,
        bgcolor=ft.colors.with_opacity(0.85, ft.colors.WHITE),
        content=ft.Column([
            ft.Text("Welcome to Plateful", size=24, weight=ft.FontWeight.BOLD, color="black"),
            ft.Text("Sign In", size=20, weight=ft.FontWeight.BOLD, color="black"),
            email_field,
            password_field,
            ft.Row([login_button], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row(
                [
                    ft.Container(width=100, content=ft.Divider(color="black")),
                    ft.Text("OR", color="black"),
                    ft.Container(width=100, content=ft.Divider(color="black")),
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Text("Don't have an account?", size=14, color="black"),
            ft.OutlinedButton(
                "Register",
                icon=ft.icons.PERSON_ADD,
                style=ft.ButtonStyle(color="black", side=ft.BorderSide(1, "black")),
                on_click=lambda _: navigate_to(page, "register")
            ),
            ft.Text("Sign In with", size=14, weight=ft.FontWeight.BOLD, color="black"),
            ft.ElevatedButton(
                text="Gmail",
                icon=ft.icons.EMAIL,
                bgcolor="white",
                color="black",
                width=300,
            ),
            ft.Row([
                ft.ElevatedButton("Facebook", icon=ft.icons.FACEBOOK, bgcolor="white", color="black", width=140),
                ft.ElevatedButton("Google", icon=ft.icons.ACCOUNT_CIRCLE_OUTLINED, bgcolor="white", color="black", width=140),
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Text(
                "By continuing, you agree to our Terms of Service, Privacy Policy, and Content Policy.",
                size=10,
                color="black",
                text_align=ft.TextAlign.CENTER,
            ),
        ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        ),
    )

    # Main container with background and form
    main_container = ft.Container(
        content=ft.Stack([
            background_image,
            ft.Container(
                content=login_form,
                alignment=ft.alignment.center,
                padding=40
            )
        ]),
        expand=True
    )

    return main_container



def registration_page(page, navigate_to):
    # Define all fields at the beginning
    username_field = ft.TextField(label="Full Name")
    contact_field = ft.TextField(label="Contact Number")
    email_field = ft.TextField(label="Email")
    location_field = ft.TextField(label="Location")

    # Additional fields for verification (initially hidden)
    student_id_field = ft.TextField(label="Student ID", visible=False)
    institution_field = ft.TextField(label="Institution", visible=False)
    bpl_card_field = ft.TextField(label="BPL Card Number", visible=False)

    user_type_field = ft.Dropdown(
        label="User Type",
        options=[
            ft.dropdown.Option(key="Admin", text="Admin"),
            ft.dropdown.Option(key="FS Employee", text="FS Employee"),
            ft.dropdown.Option(key="NGO Employee", text="NGO Employee"),
            ft.dropdown.Option(key="BPLU", text="BPL Card Holder"),
            ft.dropdown.Option(key="StudentU", text="Student"),
        ],
        on_change=lambda e: handle_user_type_change(e)
    )

    password_field = ft.TextField(label="Password", password=True)

    # Verification progress indicator
    progress_ring = ft.ProgressRing(width=20, height=20, visible=False)
    status_text = ft.Text("", color="white")
    verification_status = ft.Row(
        [progress_ring, status_text],
        alignment=ft.MainAxisAlignment.CENTER,
        visible=False
    )

    def handle_user_type_change(e):
        # Show/hide additional fields based on user type
        is_student = user_type_field.value == "StudentU"
        is_bpl = user_type_field.value == "BPLU"

        student_id_field.visible = is_student
        institution_field.visible = is_student
        bpl_card_field.visible = is_bpl

        page.update()

    async def handle_register(_):
        # Show verification in progress
        register_button.disabled = True
        verification_status.visible = True
        progress_ring.visible = True
        status_text.value = "Verifying credentials..."
        status_text.color = "white"
        page.update()

        # Get additional fields based on user type
        student_id = student_id_field.value if user_type_field.value == "StudentU" else None
        institution = institution_field.value if user_type_field.value == "StudentU" else None
        bpl_card_number = bpl_card_field.value if user_type_field.value == "BPLU" else None

        try:
            # Simulate verification delay (remove in production)
            await asyncio.sleep(1)

            success, message = register_user(
                username_field.value,
                contact_field.value,
                email_field.value,
                location_field.value,
                user_type_field.value,
                password_field.value,
                student_id,
                institution,
                bpl_card_number
            )

            if success:
                status_text.value = "Verification successful!"
                status_text.color = "green"
                page.update()

                # Wait 2 seconds before navigating
                await asyncio.sleep(2)
                navigate_to(page, "registration-success")
            else:
                status_text.value = message
                status_text.color = "red"
                register_button.disabled = False
                progress_ring.visible = False
                page.update()

        except Exception as e:
            status_text.value = f"Error: {str(e)}"
            status_text.color = "red"
            register_button.disabled = False
            progress_ring.visible = False
            page.update()

    register_button = ft.ElevatedButton(
        text="Submit",
        on_click=handle_register
    )

    return ft.Container(
        content=ft.Column([
            ft.Text("Register", size=20, weight=ft.FontWeight.BOLD),
            username_field,
            contact_field,
            email_field,
            location_field,
            user_type_field,
            student_id_field,
            institution_field,
            bpl_card_field,
            password_field,
            verification_status,
            register_button
        ])
    )


def registration_success_page(page, navigate_to):
    return ft.Container(
        content=ft.Column([
            ft.Text("Registration Successful! You can now log in."),
            ft.ElevatedButton(text="Go to Login", on_click=lambda _: navigate_to(page, "login"))
        ], alignment=ft.MainAxisAlignment.CENTER),
        alignment=ft.alignment.center,
        padding=20
    )