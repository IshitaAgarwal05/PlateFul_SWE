import flet as ft
import sqlite3

def payment_gateway_page(page: ft.Page, navigate_to, payment_details):
    donation_id = payment_details["donation_id"]
    amount = payment_details["amount"]
    ngo_id = payment_details["ngo_id"]

    def process_payment(e):
        # Here you would integrate with a real payment gateway
        # For now, we'll simulate success

        # Update payment status in database
        try:
            conn = sqlite3.connect("plateful.db")
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE DONATIONS 
                SET payment_status = 'Completed', 
                    payment_reference = 'SIMULATED_PAYMENT_123'
                WHERE donation_id = ?
            """, (donation_id,))
            conn.commit()
            conn.close()

            page.snack_bar = ft.SnackBar(ft.Text("Payment successful! Thank you for your donation."))
            page.snack_bar.open = True
            navigate_to(page, "ngo_home", ngo_id)

        except Exception as e:
            page.snack_bar = ft.SnackBar(ft.Text(f"Payment failed: {str(e)}"))
            page.snack_bar.open = True

        page.update()

    return ft.Column(
        controls=[
            ft.Text("Payment Gateway", size=24, weight="bold"),
            ft.Text(f"Donation ID: {donation_id}"),
            ft.Text(f"Amount: ₹{amount}"),
            ft.Text("Test Payment Details:"),
            ft.Text("Card: 4111 1111 1111 1111"),
            ft.Text("Expiry: 12/25, CVV: 123"),
            ft.ElevatedButton(
                "Complete Payment",
                on_click=process_payment,
                color=ft.colors.GREEN
            )
        ]
    )