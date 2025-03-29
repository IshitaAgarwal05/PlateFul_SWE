import flet as ft
import sqlite3


def get_ngo_details(ngo_id):
    conn = sqlite3.connect("plateful.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM NGO WHERE ngo_id = ?", (ngo_id,))
    ngo = cursor.fetchone()
    conn.close()
    if ngo: return (ngo[4])
    return None


def donation_page(page: ft.Page, navigate_to, ngo_id):
    # Form fields with validation
    donor_name = ft.TextField(label="Full Name", hint_text="Enter your full name")
    donor_email = ft.TextField(label="Email", hint_text="Enter your email")
    donor_aadhaar = ft.TextField(label="Aadhaar Number", hint_text="Enter 12-digit Aadhaar")
    donor_contact = ft.TextField(label="Contact Number", hint_text="Enter 10-digit mobile")
    amount = ft.TextField(
        label="Amount (₹)",
        keyboard_type=ft.KeyboardType.NUMBER,
        hint_text="Enter donation amount"
    )

    # Back button at top left
    back_button = ft.IconButton(
        icon=ft.icons.ARROW_BACK,
        icon_color=ft.colors.BLUE,
        on_click=lambda _: navigate_to(page, "ngo_desc", get_ngo_details(ngo_id)),
        tooltip="Go back",
        icon_size=30
    )

    # Validation function
    def validate_form():
        errors = []
        if not donor_name.value:
            errors.append("Full name is required")
        if not donor_email.value:
            errors.append("Email is required")
        elif "@" not in donor_email.value:
            errors.append("Valid email is required")
        if not donor_aadhaar.value or len(donor_aadhaar.value) != 12 or not donor_aadhaar.value.isdigit():
            errors.append("Valid 12-digit Aadhaar is required")
        if not donor_contact.value or len(donor_contact.value) != 10 or not donor_contact.value.isdigit():
            errors.append("Valid 10-digit contact number is required")
        if not amount.value or not amount.value.replace('.','',1).isdigit():
            errors.append("Valid amount is required")
        return errors

    def submit_donation(e):
        # Validate form
        errors = validate_form()
        if errors:
            page.snack_bar = ft.SnackBar(
                ft.Text("\n".join(errors),
                color=ft.colors.WHITE,
                bgcolor=ft.colors.RED
            ))
            page.snack_bar.open = True
            page.update()
            return

        try:
            conn = sqlite3.connect("plateful.db")
            cursor = conn.cursor()

            # Insert donation record
            cursor.execute('''
                INSERT INTO DONATIONS 
                (ngo_id, donor_name, donor_email, donor_aadhaar, donor_contact, amount)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                ngo_id,
                donor_name.value.strip(),
                donor_email.value.strip(),
                donor_aadhaar.value.strip(),
                donor_contact.value.strip(),
                float(amount.value)
            ))

            donation_id = cursor.lastrowid
            conn.commit()
            conn.close()

            # Navigate to payment gateway
            navigate_to(page, "payment_gateway", {
                "donation_id": donation_id,
                "amount": amount.value,
                "ngo_id": ngo_id
            })

        except Exception as e:
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Database error: {str(e)}"),
                color=ft.colors.WHITE,
                bgcolor=ft.colors.RED
            )
            page.snack_bar.open = True
            page.update()

    return ft.Container(
        content=ft.Column(
            controls=[
                # Header row with back button and title
                ft.Row(
                    controls=[
                        back_button,
                        ft.Text("Make a Donation", size=24, weight="bold", expand=True),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    width=page.width
                ),
                ft.Divider(height=20),

                # Form fields
                donor_name,
                donor_email,
                donor_aadhaar,
                donor_contact,
                amount,

                # Submit button
                ft.Container(
                    ft.ElevatedButton(
                        "Proceed to Payment",
                        on_click=submit_donation,
                        icon=ft.icons.PAYMENT,
                        width=300,
                        height=50,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                            padding=20
                        )
                    ),
                    alignment=ft.alignment.center
                )
            ],
            spacing=20,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=30,
        alignment=ft.alignment.top_center
    )