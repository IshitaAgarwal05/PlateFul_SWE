import sqlite3
import flet as ft


def view_donations(page: ft.Page, navigate_to, ngo_id):
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

        if not donations:
            return ft.Text("No donations received yet.")

        donation_items = []
        for d in donations:
            donation_items.append(
                ft.ListTile(
                    title=ft.Text(d[1]),  # donor_name
                    subtitle=ft.Text(f"₹{d[2]} on {d[3]}"),  # amount and date
                    trailing=ft.Text(d[4], color="green" if d[4] == "Completed" else "orange")
                )
            )

        return ft.Column(
            scroll=True,
            controls=[
                ft.Text("Your Donations", size=20, weight="bold"),
                ft.ListView(donation_items, spacing=10)
            ]
        )

    except Exception as e:
        return ft.Text(f"Error loading donations: {str(e)}")