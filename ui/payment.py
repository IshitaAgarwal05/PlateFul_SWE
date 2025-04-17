import asyncio
from datetime import datetime
import random
import flet as ft
import sqlite3
import time
import urllib
import webbrowser
from typing import Dict
from ui.user.user_menu_fs import user_carts
from ui.user.user_cart import get_food_supplier_location, create_feedback_page

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


def create_order(conn, user_id, restaurant_id, total_amount):
    """Create a new order in the database"""
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO "ORDER"
        (user_id, restaurant_id, order_time, status, total_amount) 
        VALUES (?, ?, datetime('now'), 'pending', ?)""",
        (user_id, restaurant_id, total_amount)
    )
    return cursor.lastrowid


def add_order_items(conn, order_id, cart):
    """Add items to the ORDER_ITEM table"""
    cursor = conn.cursor()
    for item_id, quantity in cart.items():
        item_details = get_item_details(item_id)
        if item_details:
            cursor.execute(
                """INSERT INTO ORDER_ITEM 
                (order_id, food_item_id, quantity, unit_price) 
                VALUES (?, ?, ?, ?)""",
                (order_id, item_id, quantity, item_details['price'])
            )


def record_payment(conn, order_id, amount, payment_method, status):
    """Record payment in the PAYMENT table"""
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO PAYMENT 
        (order_id, amount, payment_method, status, payment_time) 
        VALUES (?, ?, ?, ?, datetime('now'))""",
        (order_id, amount, payment_method, status)
    )


def payment_page(page: ft.Page, navigate_to, email, amount=None, cart=None, restaurant_id=None):
    """Simplified payment page with direct flow"""
    if amount is None:
        amount = 0.0

    # Payment method selection
    selected_payment_method = ft.RadioGroup(
        value='card',
        content=ft.Column([
            ft.Container(
                content=ft.ListTile(
                    leading=ft.Radio(value="card"),
                    title=ft.Text("Credit/Debit Card"),
                    trailing=ft.Icon(ft.icons.CREDIT_CARD),
                ),
                padding=10,
                bgcolor=ft.colors.WHITE,
                border_radius=10,
                margin=5
            ),
            ft.Container(
                content=ft.ListTile(
                    leading=ft.Radio(value="upi"),
                    title=ft.Text("UPI Payment"),
                    trailing=ft.Icon(ft.icons.PAYMENTS),
                ),
                padding=10,
                bgcolor=ft.colors.WHITE,
                border_radius=10,
                margin=5
            ),
            ft.Container(
                content=ft.ListTile(
                    leading=ft.Radio(value="cod"),
                    title=ft.Text("Cash on Delivery"),
                    trailing=ft.Icon(ft.icons.LOCAL_ATM),
                ),
                padding=10,
                bgcolor=ft.colors.WHITE,
                border_radius=10,
                margin=5
            ),
        ], spacing=5)
    )

    processing = ft.Ref[bool]()  # To track processing state
    processing.current = False

    def pay_now(e):
        processing.current = True
        page.update()

        try:
            user_id = get_user_id(email)
            if not user_id:
                raise Exception("User ID not found")

            conn = sqlite3.connect("plateful.db")

            # Create and add order items; record payment
            order_id = create_order(conn, user_id, restaurant_id, amount)
            add_order_items(conn, order_id, cart)
            record_payment(conn, order_id, amount, selected_payment_method.value, "completed")

            conn.commit()
            conn.close()

            # Clear cart
            if email in user_carts:
                del user_carts[email]

            # Open maps
            supplier = get_food_supplier_location(restaurant_id)
            if supplier:
                maps_url = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(supplier['name'] + ' ' + supplier['location'])}"
                webbrowser.open(maps_url)

            # Feedback
            feedback_page = create_feedback_page(page, navigate_to, email, restaurant_id)
            page.clean()
            page.add(feedback_page)
            page.update()

        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {str(ex)}"))
            page.snack_bar.open = True
            page.update()

    def cancel_payment(e):
        navigate_to(page, "user_cart", email, restaurant_id)

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Payment Options", size=24, weight="bold"),
                ft.Divider(),

                # Amount display
                ft.Container(
                    content=ft.Column([
                        ft.Text("Total Amount", size=16),
                        ft.Text(f"₹{amount:.2f}", size=36, weight="bold")
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=20,
                    bgcolor=ft.colors.WHITE,
                    border_radius=10,
                    margin=ft.margin.only(bottom=20)
                ),

                # Payment methods
                ft.Text("Select Payment Method:", size=16, weight="bold"),
                selected_payment_method,

                # Processing indicator
                ft.Container(
                    content=ft.ProgressRing(visible=False),
                    ref=lambda r: setattr(processing, 'indicator', r),
                    padding=20,
                    alignment=ft.alignment.center
                ),

                # Action buttons
                ft.Row([
                    ft.OutlinedButton(
                        "Cancel",
                        on_click=cancel_payment,
                        icon=ft.icons.ARROW_BACK,
                        disabled=lambda: processing.current
                    ),
                    ft.ElevatedButton(
                        "Confirm Payment",
                        on_click=pay_now,
                        icon=ft.icons.LOCK,
                        style=ft.ButtonStyle(
                            bgcolor=ft.colors.GREEN,
                            color=ft.colors.WHITE,
                            padding=ft.padding.symmetric(horizontal=30, vertical=15)
                        ),
                        disabled=lambda: processing.current
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)
            ],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO  # Make the page scrollable
        ),
        padding=30,
        expand=True
    )

# Helper function to get user_id from email
def get_user_id(email):
    conn = sqlite3.connect("plateful.db")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM USER WHERE email = ?", (email,))
        result = cursor.fetchone()
        return result[0] if result else None
    finally:
        conn.close()


# Helper function to get item details
def get_item_details(item_id):
    conn = sqlite3.connect("plateful.db")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name, price FROM FOOD_ITEM WHERE item_id = ?", (item_id,))
        result = cursor.fetchone()
        return {"name": result[0], "price": result[1]} if result else None
    finally:
        conn.close()