import sqlite3
import flet as ft


def get_ngo_details(ngo_id):
    conn = sqlite3.connect("plateful.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM NGO WHERE ngo_id = ?", (ngo_id,))
    ngo = cursor.fetchone()
    conn.close()
    if ngo: return (ngo[4])
    return None


def view_donations(page: ft.Page, navigate_to, ngo_id):
    back_button = ft.IconButton(
        icon=ft.icons.ARROW_BACK,
        icon_color=ft.colors.BLUE,
        on_click=lambda _: navigate_to(page, "ngo_desc", get_ngo_details(ngo_id)),
        tooltip="Go back",
        icon_size=30
    )

    try:
        conn = sqlite3.connect("plateful.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT donation_id, donor_name, amount, donation_date, payment_status
            FROM DONATIONS
            WHERE ngo_id = ?
            ORDER BY donation_date DESC
        """, (ngo_id,))

        donations = cursor.fetchall()
        conn.close()

        content = [
            # Header with back button
            ft.Row(
                controls=[
                    back_button,
                    ft.Text("Your Donations", size=24, weight="bold", expand=True)
                ],
                alignment=ft.MainAxisAlignment.START,
                width=page.width
            ),
            ft.Divider(height=20)
        ]

        if not donations:
            content.append(ft.Text("No donations received yet."))
        else:
            for d in donations:
                content.append(
                    ft.ListTile(
                        title=ft.Text(d[1]),  # donor_name
                        subtitle=ft.Text(f"₹{d[2]} on {d[3]}"),  # amount and date
                        trailing=ft.Text(
                            d[4],
                            color="green" if d[4] == "Completed" else "orange"
                        )
                    )
                )

        return ft.Container(
            content=ft.Column(
                content,
                spacing=20,
                scroll=ft.ScrollMode.AUTO
            ),
            padding=30
        )


    except Exception as e:
        return ft.Column(
            controls=[
                ft.Row([back_button, ft.Text("Error", size=24)]),
                ft.Text(f"Error loading donations: {str(e)}", color="red")
            ],
            spacing=20
        )