import flet as ft
import time

def main(page: ft.Page):
    # Set strict mobile-specific page configuration
    page.title = "Student Registration"
    page.theme = ft.Theme(font_family="Roboto")
    page.padding = 0
    page.window_width = 360
    page.window_height = 640
    page.window_resizable = False
    
    # List to store verification code inputs
    verification_codes = [ft.TextField() for _ in range(6)]

    # Timer state
    remaining_seconds = 60
    timer_text = ft.Text("1:00", color="white", size=14, weight="bold")
    timer_running = False

    def on_verification_change(e, index):
        field = verification_codes[index]
        value = field.value or ""
        
        if value:
            if not value.isdigit():
                field.value = "".join(char for char in value if char.isdigit())
                field.update()
                return
            if len(value) > 1:
                field.value = value[-1]
                field.update()
        
        if value and len(value) == 1 and index < 5:
            verification_codes[index + 1].focus()
            verification_codes[index + 1].value = ""
            verification_codes[index + 1].update()
        elif not value and index > 0:
            verification_codes[index - 1].focus()

    def update_timer():
        nonlocal remaining_seconds, timer_running
        if timer_running and remaining_seconds > 0:
            remaining_seconds -= 1
            minutes = remaining_seconds // 60
            seconds = remaining_seconds % 60
            timer_text.value = f"{minutes}:{seconds:02d}"
            page.update()
            page.run_task(lambda: time.sleep(1) or update_timer())
        elif timer_running and remaining_seconds <= 0:
            timer_running = False
            timer_text.value = "0:00"
            page.update()

    def show_otp_dialog(e):
        nonlocal remaining_seconds, timer_running
        if not timer_running:  # Only start if not already running
            # Reset and start timer
            remaining_seconds = 60
            timer_text.value = "1:00"
            timer_running = True
            page.update()
            update_timer()
            
            # Create and show dialog
            dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("OTP Sent"),
                content=ft.Text("OTP has been sent to your registered mobile number"),
                actions=[
                    ft.TextButton("OK", on_click=lambda e: close_dialog())
                ],
                actions_alignment=ft.MainAxisAlignment.END
            )
            page.dialog = dialog
            dialog.open = True
            page.update()

    def close_dialog():
        page.dialog.open = False
        page.update()

    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.icons.ARROW_BACK,
                                icon_color="white",
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                    padding=ft.Padding(8, 8, 8, 8)
                                ),
                                icon_size=20
                            ),
                            ft.Text(
                                "Registration of Student",
                                size=16,
                                color="white",
                                weight="bold"
                            )
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=5
                    ),
                    ft.Container(
                        padding=10,
                        bgcolor="white",
                        border_radius=8,
                        width=340,
                        content=ft.Column(
                            [
                                ft.TextField(
                                    label="Name",
                                    border_color="transparent",
                                    filled=True,
                                    fill_color="#f5f5f5",
                                    height=40,
                                    text_size=14,
                                    width=320,
                                    text_style=ft.TextStyle(color="black")
                                ),
                                ft.TextField(
                                    label="Mobile No.",
                                    border_color="transparent",
                                    filled=True,
                                    fill_color="#f5f5f5",
                                    height=40,
                                    text_size=14,
                                    width=320,
                                    text_style=ft.TextStyle(color="black")
                                ),
                                ft.TextField(
                                    label="Email",
                                    border_color="transparent",
                                    filled=True,
                                    fill_color="#f5f5f5",
                                    height=40,
                                    text_size=14,
                                    width=320,
                                    text_style=ft.TextStyle(color="black")
                                ),
                                ft.TextField(
                                    label="School/College ID",
                                    border_color="transparent",
                                    filled=True,
                                    fill_color="#f5f5f5",
                                    height=40,
                                    text_size=14,
                                    width=320,
                                    text_style=ft.TextStyle(color="black")
                                ),
                                ft.TextField(
                                    label="Address",
                                    border_color="transparent",
                                    filled=True,
                                    fill_color="#f5f5f5",
                                    height=80,
                                    multiline=True,
                                    min_lines=3,
                                    text_size=14,
                                    width=320,
                                    text_style=ft.TextStyle(color="black")
                                ),
                            ],
                            spacing=10
                        )
                    ),
                    ft.Container(
                        padding=10,
                        width=340,
                        content=ft.Column(
                            [
                                # Second Generate OTP button added here
                                ft.ElevatedButton(
                                    "Generate OTP",
                                    bgcolor="black",
                                    color="white",
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=8),
                                        padding=ft.Padding(12, 8, 12, 8)
                                    ),
                                    width=180,
                                    on_click=show_otp_dialog
                                ),
                                ft.Text(
                                    "We have sent a verification code to",
                                    color="white",
                                    size=12
                                ),
                                ft.Text(
                                    "+91-9010858965",
                                    color="white",
                                    weight="bold",
                                    size=14
                                ),
                                ft.Row(
                                    [
                                        ft.TextField(
                                            key=f"verify_{i}",
                                            width=40,
                                            height=40,
                                            border_color="white",
                                            text_align="center",
                                            fill_color="white",
                                            border_radius=8,
                                            text_size=16,
                                            text_style=ft.TextStyle(color="black"),
                                            max_length=1,
                                            keyboard_type=ft.KeyboardType.NUMBER,
                                            on_change=lambda e, idx=i: on_verification_change(e, idx)
                                        ) for i in range(6)
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=5
                                ),
                                timer_text,
                                ft.ElevatedButton(
                                    "Submit",
                                    bgcolor="black",
                                    color="white",
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=8),
                                        padding=ft.Padding(12, 8, 12, 8)
                                    ),
                                    width=200
                                ),
                                ft.TextButton(
                                    "Didn't receive the code? Resend now",
                                    style=ft.ButtonStyle(
                                        color={"": "white"},
                                        text_style=ft.TextStyle(size=12)
                                    )
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=10
                        )
                    )
                ],
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            gradient=ft.LinearGradient(
                begin=ft.Alignment(-1.0, -1.0),
                end=ft.Alignment(1.0, 1.0),
                colors=["#ff4d4d", "#ff8c1a"]
            ),
            width=360,
            height=640
        )
    )

ft.app(target=main)