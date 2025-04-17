import flet as ft
import sqlite3
from typing import Dict, Optional
from ui.user.user_menu_fs import user_carts
import webbrowser
import urllib.parse
import time


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


def create_feedback_page(page: ft.Page, navigate_to, email: str, restaurant_id: int) -> ft.Container:
    """Create the feedback rating interface"""
    food_rating = ft.Ref[ft.Row]()
    service_rating = ft.Ref[ft.Row]()

    def submit_feedback(e):
        # Calculate ratings
        food_stars = sum(1 for star in food_rating.current.controls if star.icon_color == ft.colors.AMBER)
        service_stars = sum(1 for star in service_rating.current.controls if star.icon_color == ft.colors.AMBER)
        average_rating = (food_stars + service_stars) / 2

        # Update database
        conn = sqlite3.connect("plateful.db")
        try:
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE FOOD_SUPPLIER 
                SET rating = COALESCE((rating * rating_count + ?) / (rating_count + 1), ?),
                    rating_count = COALESCE(rating_count, 0) + 1
                WHERE restaurant_id = ?""",
                (average_rating, average_rating, restaurant_id)
            )
            conn.commit()

            page.snack_bar = ft.SnackBar(
                content=ft.Text("Thank you for your feedback!"),
                bgcolor=ft.colors.GREEN
            )
            page.snack_bar.open = True
            page.update()

            time.sleep(2)
            navigate_to(page, "user_home", email)
        finally:
            conn.close()

    def create_star_rating(ref, label: str) -> ft.Column:
        def star_click(e, index: int):
            for i, star in enumerate(ref.current.controls):
                star.icon_color = ft.colors.AMBER if i <= index else ft.colors.GREY
            page.update()

        stars = ft.Row(
            ref=ref,
            controls=[
                ft.IconButton(
                    icon=ft.icons.STAR,
                    icon_color=ft.colors.GREY,
                    on_click=lambda e, i=i: star_click(e, i)
                )
                for i in range(5)
            ],
            spacing=5
        )

        return ft.Container(
            content=ft.Column([
                ft.Text(label, size=16, weight="bold", color=ft.colors.BLACK),
                stars
            ], spacing=10),
            bgcolor=ft.colors.WHITE,
            padding=15,
            border_radius=10,
            margin=ft.margin.symmetric(vertical=5)
        )


    return ft.Container(
        bgcolor="#FF6F4F",
        content=ft.Column([
            ft.Text("Share Your Experience", size=28, weight="bold", color=ft.colors.WHITE),
            ft.Divider(color=ft.colors.AMBER_400),

            ft.Container(
                width=300,
                height=180,
                border_radius=15,
                padding=50,
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_left,
                    end=ft.alignment.bottom_right,
                    colors=[ft.colors.BLUE_800, ft.colors.PURPLE_800]
                ),
                content=ft.Column([
                    ft.Icon(ft.icons.RESTAURANT, size=50, color=ft.colors.AMBER_100),
                    ft.Text("How was your visit?", size=18, color=ft.colors.WHITE)
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            ),

            create_star_rating(food_rating, "Food Quality"),
            create_star_rating(service_rating, "Service Quality"),

            ft.ElevatedButton(
                "Submit Feedback",
                icon=ft.icons.SEND,
                on_click=submit_feedback,
                bgcolor=ft.colors.AMBER,
                color=ft.colors.WHITE,
                width=200,
                height=45
            )
        ],
            spacing=25,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO),
        padding=30,
        expand=True
    )


def checkout_flow(page: ft.Page, navigate_to, email: str, restaurant_id: int):
    """Handle the complete checkout process"""
    if email in user_carts:
        del user_carts[email]

    supplier = get_food_supplier_location(restaurant_id)
    if supplier:
        maps_url = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(supplier['name'] + ' ' + supplier['location'])}"
        webbrowser.open(maps_url)

    # Immediately show feedback page
    feedback_page = create_feedback_page(page, navigate_to, email, restaurant_id)
    page.clean()
    page.add(feedback_page)
    page.update()


def cart_page(page: ft.Page, navigate_to, email, food_supplier_id):
    """Main cart page with checkout functionality"""
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
        "Proceed to Payment",
        on_click=lambda _: navigate_to(
            page,
            "payment_gateway",
            email,
            {"amount": total_amount, "cart": cart, "restaurant_id": food_supplier_id}
        ),
        icon=ft.icons.PAYMENT,
        style=ft.ButtonStyle(
            bgcolor=ft.colors.GREEN,
            color=ft.colors.WHITE
        )
    )

    # checkout_btn = ft.ElevatedButton(
    #     "Checkout",
    #     on_click=lambda _: checkout_flow(page, navigate_to, email, food_supplier_id),
    #     icon=ft.icons.MAP,
    #     width=180,
    #     style=ft.ButtonStyle(bgcolor=ft.colors.GREEN, color=ft.colors.WHITE)
    # )

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