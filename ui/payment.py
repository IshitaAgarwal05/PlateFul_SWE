# import flet as ft
# import sqlite3

# def payment_gateway_page(page: ft.Page, navigate_to, payment_details):
#     donation_id = payment_details["donation_id"]
#     amount = payment_details["amount"]
#     ngo_id = payment_details["ngo_id"]

#     def process_payment(e):
#         # Here you would integrate with a real payment gateway
#         # For now, we'll simulate success


#         # Update payment status in database
#         try:
#             conn = sqlite3.connect("plateful.db")
#             cursor = conn.cursor()
#             cursor.execute("""
#                 UPDATE DONATIONS
#                 SET payment_status = 'Completed',
#                     payment_reference = 'SIMULATED_PAYMENT_123'
#                 WHERE donation_id = ?
#             """, (donation_id,))
#             conn.commit()
#             conn.close()

#             page.snack_bar = ft.SnackBar(ft.Text("Payment successful! Thank you for your donation."))
#             page.snack_bar.open = True
#             navigate_to(page, "ngo_home", ngo_id)

#         except Exception as e:
#             page.snack_bar = ft.SnackBar(ft.Text(f"Payment failed: {str(e)}"))
#             page.snack_bar.open = True

#         page.update()

#     return ft.Column(
#         controls=[
#             ft.Text("Payment Gateway", size=24, weight="bold"),
#             ft.Text(f"Donation ID: {donation_id}"),
#             ft.Text(f"Amount: ₹{amount}"),
#             ft.Text("Test Payment Details:"),
#             ft.Text("Card: 4111 1111 1111 1111"),
#             ft.Text("Expiry: 12/25, CVV: 123"),
#             ft.ElevatedButton(
#                 "Complete Payment",
#                 on_click=process_payment,
#                 color=ft.colors.GREEN
#             )
#         ]
#     )



import asyncio
from datetime import datetime
import random
import flet as ft


async def process_payment(amount, currency='INR', payment_method='card'):
    """Simulate payment processing with 90% success rate"""
    await asyncio.sleep(2)  # Simulate network delay
    is_success = random.randint(1, 10) != 1

    if is_success:
        return {
            'status': 'success',
            'message': 'Payment processed successfully',
            'transactionId': f'SIM{int(datetime.now().timestamp() * 1000)}',
            'amount': amount,
            'currency': currency,
            'timestamp': datetime.now().isoformat(),
            'paymentMethod': payment_method,
        }
    else:
        raise Exception('Payment failed! Please try again.')


def payment_page(page: ft.Page, navigate_to, email, amount=None):
    """Payment gateway page that integrates with main app navigation"""

    # Default amount if not provided
    if amount is None:
        amount = 0.0

    selected_payment_method = ft.RadioGroup(
        value='card',
        content=ft.Column([
            ft.Radio(value='card', label='Credit/Debit Card'),
            ft.Radio(value='upi', label='UPI'),
        ])
    )

    processing_btn = ft.Ref[ft.TextButton]()
    amount_display = ft.Ref[ft.Text]()

    async def on_payment_success(result):
        page.snack_bar = ft.SnackBar(
            ft.Text(f"Payment Successful! Transaction ID: {result['transactionId']}"),
            bgcolor=ft.colors.GREEN
        )
        page.snack_bar.open = True
        page.update()
        # Navigate back to appropriate page after payment
        navigate_to(page, "user_home", email)

    async def on_payment_failure(error_message):
        page.snack_bar = ft.SnackBar(
            ft.Text(error_message),
            bgcolor=ft.colors.RED
        )
        page.snack_bar.open = True
        page.update()

    async def pay_now(e):
        processing_btn.current.text = 'Processing...'
        processing_btn.current.disabled = True
        page.update()

        try:
            result = await process_payment(
                amount,
                payment_method=selected_payment_method.value
            )
            await on_payment_success(result)
        except Exception as e:
            await on_payment_failure(str(e))
        finally:
            processing_btn.current.text = 'Pay Now'
            processing_btn.current.disabled = False
            page.update()

    def cancel_payment(e):
        navigate_to(page, "user_home", email)

    # Update amount display if it changes
    if hasattr(page, 'payment_amount'):
        amount = page.payment_amount
        if amount_display.current:
            amount_display.current.value = f'Amount to Pay: ₹{amount:.2f}'
            page.update()

    return ft.Column(
        controls=[
            ft.Text(
                f'Amount to Pay: ₹{amount:.2f}',
                size=20,
                weight=ft.FontWeight.BOLD,
                ref=amount_display
            ),
            ft.Text('Select Payment Method:'),
            selected_payment_method,
            ft.Row([
                ft.TextButton(
                    'Pay Now',
                    on_click=pay_now,
                    ref=processing_btn,
                    style=ft.ButtonStyle(
                        color=ft.colors.WHITE,
                        bgcolor=ft.colors.ORANGE_800
                    )
                ),
                ft.TextButton(
                    'Cancel',
                    on_click=cancel_payment,
                    style=ft.ButtonStyle(
                        color=ft.colors.WHITE,
                        bgcolor=ft.colors.RED_600
                    )
                )
            ], alignment=ft.MainAxisAlignment.CENTER)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )