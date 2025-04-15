import flet as ft
import sqlite3
from typing import Dict, Optional
from ui.user.user_menu_fs import user_carts
import webbrowser
import urllib.parse
import time


# Shared carty storage
user_carts  ={}

def get_item_details(item_id: int) -> Dict:
    """Get details for a specific menu item"""
    conn = sqlite3.connect("plateful.db")
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT name, price FROM FOOD_ITEM WHERE item_id = ?",
            (item_id,)
        )
        result = cursor.fetchone()
        if result:
            return {
                "name": result[0],
                "price": result[1]
            }
        return None
    finally:
        conn.close()


def get_food_supplier_location(food_supplier_id: int) -> Dict:
    """Get food supplier name and location for maps"""
    conn = sqlite3.connect("plateful.db")
    cursor = conn.cursor()
    try:
        print(f"Searching for supplier ID: {food_supplier_id}")  # Debug

        cursor.execute(
            "SELECT name, location FROM FOOD_SUPPLIER WHERE restaurant_id = ?",
            (food_supplier_id,)
        )
        result = cursor.fetchone()

        print(f"Database result: {result}")  # Debug

        if result:
            return {
                "name": result[0],
                "location": result[1]
            }
        return None
    except Exception as e:
        print(f"Database error: {e}")  # Debug
        return None
    finally:
        conn.close()


def cart_page(page: ft.Page, navigate_to, email, food_supplier_id):
    cart = user_carts.get(email, {})

    def get_cart_items():
        items = []
        for item_id, quantity in cart.items():
            details = get_item_details(item_id)
            if details:
                items.append({
                    "item_id": item_id,
                    "name": details["name"],
                    "price": details["price"],
                    "quantity": quantity,
                    "total": details["price"] * quantity
                })
        return items

    def open_maps(e):
        """Open Google Maps with food supplier location"""
        print("Checkout button clicked!")  # Debug print
        try:
            supplier = get_food_supplier_location(food_supplier_id)
            print(f"Supplier data: {supplier}")  # Debug print

            if not supplier:
                print("No supplier found")  # Debug print
                page.snack_bar = ft.SnackBar(
                    ft.Text("Supplier location not found!"),
                    open=True
                )
                page.update()
                return

            # Properly encode the query for URL
            query = urllib.parse.quote_plus(f"{supplier['name']}, {supplier['location']}, Jaipur")
            maps_url = f"https://www.google.com/maps/search/?api=1&query={query}"
            print(f"Opening URL: {maps_url}")  # Debug print

            # Try multiple methods to open the URL
            try:
                # Method 1: Using webbrowser
                webbrowser.open(maps_url)

                # Method 2: Using page.launch_url (for web)
                # page.launch_url(maps_url)

                # Show confirmation to user
                page.snack_bar = ft.SnackBar(
                    ft.Text(f"Opening directions to {supplier['name']}"),
                    open=True
                )
            except Exception as e:
                print(f"Error opening URL: {e}")  # Debug print
                page.snack_bar = ft.SnackBar(
                    ft.Text(f"Failed to open maps: {e}"),
                    open=True
                )

            page.update()

        except Exception as e:
            print(f"Error in open_maps: {e}")  # Debug print
            page.snack_bar = ft.SnackBar(
                ft.Text(f"An error occurred: {e}"),
                open=True
            )
            page.update()

    cart_items = get_cart_items()
    subtotal = sum(item["total"] for item in cart_items)
    platform_fee = 5.00
    gst = subtotal * 0.18
    total_amount = subtotal + platform_fee + gst

    def update_quantity(item_id, new_quantity):
        if new_quantity <= 0:
            cart.pop(item_id, None)
        else:
            cart[item_id] = new_quantity
        # Refresh the cart page
        navigate_to(page, "user_cart", email, food_supplier_id)

    if not cart_items:
        return ft.Column([
            ft.Text("Your cart is empty", size=20),
            ft.ElevatedButton(
                "Back to Restaurants",
                on_click=lambda _: navigate_to(page, "user_home", email)
            )
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    item_rows = []
    for item in cart_items:
        item_rows.append(
            ft.Row([
                ft.Text(f"{item['name']}", size=14, expand=2),
                ft.Text(f"₹{item['price']:.2f}", size=14, expand=1),
                ft.Row([
                    ft.IconButton(
                        ft.icons.REMOVE,
                        on_click=lambda e, id=item['item_id']: update_quantity(id, item['quantity'] - 1),
                        icon_size=20
                    ),
                    ft.Text(str(item['quantity']), size=14),
                    ft.IconButton(
                        ft.icons.ADD,
                        on_click=lambda e, id=item['item_id']: update_quantity(id, item['quantity'] + 1),
                        icon_size=20
                    ),
                ], spacing=0, expand=1),
                ft.Text(f"₹{item['total']:.2f}", size=14, expand=1)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        )

    checkout_btn = ft.ElevatedButton(
        "Checkout",
        on_click=open_maps,  # Just pass the function reference
        color=ft.colors.WHITE,
        bgcolor=ft.colors.GREEN,
        expand=True
    )

    # Add this temporary debug button
    # debug_btn = ft.ElevatedButton(
    #     "Test Maps Open",
    #     on_click=lambda e: page.launch_url("https://google.com"),
    #     color=ft.colors.WHITE,
    #     bgcolor=ft.colors.BLUE,
    #     expand=True
    # )

    return ft.Column([
        ft.Text("Your Cart", size=24, weight="bold"),
        ft.Column(
            controls=item_rows,
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
            expand=True
        ),
        ft.Divider(),
        # Charges breakdown
        ft.Row([
            ft.Text("Subtotal:", size=14),
            ft.Text(f"₹{subtotal:.2f}", size=14)
        ], alignment=ft.MainAxisAlignment.END),
        ft.Row([
            ft.Text("Platform Fee:", size=14),
            ft.Text(f"₹{platform_fee:.2f}", size=14)
        ], alignment=ft.MainAxisAlignment.END),
        ft.Row([
            ft.Text("GST (18%):", size=14),
            ft.Text(f"₹{gst:.2f}", size=14)
        ], alignment=ft.MainAxisAlignment.END),
        ft.Divider(),
        # Total
        ft.Row([
            ft.Text("Total:", size=16, weight="bold"),
            ft.Text(f"₹{total_amount:.2f}", size=16, weight="bold")
        ], alignment=ft.MainAxisAlignment.END),
        ft.Row([
            ft.ElevatedButton(
                "Continue Shopping",
                on_click=lambda _: navigate_to(page, "user_home", email),
                expand=True
            ),
            checkout_btn,
            # debug_btn
        ], spacing=20)
    ], spacing=20)

