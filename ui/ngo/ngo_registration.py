import flet as ft

def main(page: ft.Page):
    page.title = "NGO Registration"
    page.bgcolor = "#F8F8F8"
    page.padding = 10
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Back Button
    back_button = ft.IconButton(
        icon=ft.icons.ARROW_BACK,
        icon_color="black",
        on_click=lambda e: print("Back clicked"),
    )

    # Input Fields
    input_fields = [
        ("NGO Name", ""),
        ("Employee Name", ""),
        ("Employee ID", ""),
        ("Email ID", ""),
        ("Mobile No.", ""),
        ("Address", ""),
    ]

    inputs = [ft.TextField(label=label, bgcolor="white", border_radius=8, width=300) for label, _ in input_fields]

    # Submit Button
    submit_button = ft.ElevatedButton(
        text="Submit",
        bgcolor="black",
        color="white",
        width=300,
    )

    # OTP Section
    otp_text = ft.Text(
        "We have sent a verification code to\n+91-9010858965",
        size=14,
        text_align=ft.TextAlign.CENTER,
    )

    otp_boxes = ft.Row(
        [ft.TextField(width=40, text_align=ft.TextAlign.CENTER) for _ in range(6)],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    timer = ft.Text("0:19", size=14, text_align=ft.TextAlign.CENTER)

    resend_text = ft.Row(
        [
            ft.Text("Didn't receive the code?", size=12),
            ft.TextButton("Resend now", on_click=lambda e: print("Resend clicked")),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # Main Container
    main_container = ft.Container(
        padding=20,
        bgcolor=ft.LinearGradient(
            colors=["#D84315", "#FF9800"],  # Gradient color matching the design
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center
        ),
        border_radius=20,
        content=ft.Column(
            [
                back_button,
                ft.Container(
                    padding=15,
                    bgcolor="white",
                    border_radius=10,
                    content=ft.Column(inputs, spacing=10),
                ),
                submit_button,
                otp_text,
                otp_boxes,
                timer,
                resend_text,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        ),
    )

    page.add(main_container)

ft.app(target=main)
