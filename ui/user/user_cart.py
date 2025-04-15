import flet as ft
import sqlite3
import webbrowser
from typing import Dict
from ui.user.user_menu_fs import user_carts


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


def get_food_supplier_location(restaurant_id: int) -> Dict:
    """Get food supplier name and location for maps"""
    conn = sqlite3.connect("plateful.db")
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT name, location FROM FOOD_SUPPLIER WHERE restaurant_id = ?",
            (restaurant_id,)
        )
        result = cursor.fetchone()
        if result:
            return {
                "name": result[0],
                "location": result[1]
            }
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
        supplier = get_food_supplier_location(food_supplier_id)
        if supplier:
            # Create a maps URL with the supplier's name and location
            query = f"{supplier['name']}, {supplier['location']}, Jaipur"
            maps_url = f"https://www.google.com/maps/search/?api=1&query={query}"
            # Open the URL in default browser
            webbrowser.open(maps_url)

            # Alternative: Show confirmation dialog
            page.dialog = ft.AlertDialog(
                title=ft.Text("Opening Maps"),
                content=ft.Text(f"Opening directions to {supplier['name']}"),
                on_dismiss=lambda e: print("Dialog dismissed")
            )
            page.dialog.open = True
        else:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Could not find supplier location"),
                action="OK"
            )
            page.snack_bar.open = True
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
            ft.ElevatedButton(
                "Checkout",
                on_click=lambda e: open_maps,
                color=ft.colors.WHITE,
                bgcolor=ft.colors.GREEN,
                expand=True
            )
        ], spacing=20)
    ], spacing=20)