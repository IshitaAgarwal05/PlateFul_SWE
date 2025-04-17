import flet as ft
import sqlite3
from typing import Optional, Dict, List
from db.models import get_user_type, update_food_item_quantity

# Global variable to store cart items
user_carts = {}


def get_supplier_menu_with_dynamic_pricing(restaurant_id: int, user_type: str) -> Optional[Dict]:
    """Get food supplier menu with dynamic pricing and quantity info"""
    conn = sqlite3.connect("plateful.db")
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT name, location, contact, rating, description FROM FOOD_SUPPLIER "
            "WHERE restaurant_id = ?",
            (restaurant_id,)
        )
        supplier_data = cursor.fetchone()

        if not supplier_data:
            print(f"No supplier found with ID: {restaurant_id}")
            return None

        cursor.execute(
            "SELECT item_id, name, price, description, quantity FROM FOOD_ITEM "
            "WHERE restaurant_id = ? AND available = 1 AND quantity > 0",
            (restaurant_id,)
        )
        menu_items = cursor.fetchall()

        # Apply discounts based on user type
        discounted_menu = []
        for item in menu_items:
            original_price = item[2]
            quantity = item[4]

            if user_type == "StudentU":
                discounted_price = original_price * 0.6
            elif user_type == "BPLU":
                discounted_price = original_price * 0.3
            elif user_type == "NGO Employee":
                discounted_price = original_price * 0.5
            else:
                discounted_price = original_price

            discounted_menu.append({
                "item_id": item[0],
                "name": item[1],
                "original_price": original_price,
                "discounted_price": discounted_price,
                "description": item[3],
                "available_quantity": quantity
            })

        return {
            "restaurant_id": restaurant_id,
            "name": supplier_data[0],
            "location": supplier_data[1],
            "contact": supplier_data[2],
            "rating": supplier_data[3],
            "description": supplier_data[4],
            "menu": discounted_menu,
            "user_type": user_type
        }
    except Exception as e:
        print(f"Error fetching supplier menu: {e}")
        return None
    finally:
        conn.close()


def create_menu_item_card(item: Dict, cart: Dict, page: ft.Page, update_cart_fn) -> ft.Card:
    """Create a card for a single menu item with cart functionality"""
    quantity = cart.get(item['item_id'], 0)
    quantity_text = ft.Text(str(quantity), size=14, weight="bold")
    available_quantity = item.get('available_quantity', 0)

    def update_quantity(increment):
        new_quantity = max(0, quantity + increment)
        if new_quantity > available_quantity:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Only {available_quantity} available!", color="white"),
                bgcolor="red"
            )
            page.snack_bar.open = True
            return

        if new_quantity == 0:
            cart.pop(item['item_id'], None)
        else:
            cart[item['item_id']] = new_quantity
        quantity_text.value = str(new_quantity)
        page.update()
        update_cart_fn()

    # Price display
    price_display = ft.Column(spacing=0)
    if 'original_price' in item and 'discounted_price' in item:
        if item['original_price'] != item['discounted_price']:
            price_display.controls.extend([
                ft.Text(
                    f"₹{item['original_price']:.2f}",
                    size=12,
                    color=ft.colors.GREY_500,
                    # spans=[ft.TextSpan(style=ft.TextDecoration.LINE_THROUGH)]
                ),
                ft.Text(f"₹{item['discounted_price']:.2f}", size=14, color=ft.colors.GREEN)
            ])
        else:
            price_display.controls.append(ft.Text(f"₹{item['original_price']:.2f}", size=14))

    # Quantity available display
    quantity_display = ft.Text(f"Available: {available_quantity}", size=12, color=ft.colors.BLUE)

    # Image handling
    image = ft.Container(
        width=100,
        height=80,
        border_radius=10,
        content=ft.Image(
            src=f"assets/images/fs/{item['item_id']}.png",
            fit=ft.ImageFit.COVER,
            error_content=ft.Icon(ft.icons.FASTFOOD, size=40)
        )
    )

    return ft.Card(
        content=ft.Container(
            content=ft.Row([
                image,
                ft.Column([
                    ft.Text(item['name'], size=16, weight="bold"),
                    price_display,
                    quantity_display,
                    ft.Text(
                        item.get('description', 'No description available'),
                        size=12,
                        color=ft.colors.GREY_600,
                        max_lines=2
                    )
                ], spacing=5, expand=True),
                ft.Row([
                    ft.IconButton(
                        ft.icons.REMOVE,
                        on_click=lambda e: update_quantity(-1),
                        icon_size=20,
                        disabled=quantity <= 0
                    ),
                    quantity_text,
                    ft.IconButton(
                        ft.icons.ADD,
                        on_click=lambda e: update_quantity(1),
                        icon_size=20,
                        disabled=quantity >= available_quantity
                    ),
                ], spacing=0)
            ], spacing=15),
            padding=15,
            width=400
        ),
        elevation=3,
        margin=ft.margin.symmetric(vertical=5)
    )


def user_menu_page(page: ft.Page, navigate_to, email, restaurant_id: int, user_type) -> ft.Column:
    """Main page showing food supplier's menu to users"""
    if email not in user_carts:
        user_carts[email] = {}
    cart = user_carts[email]

    # Initialize controls first
    cart_summary = ft.Row(
        visible=False,
        controls=[
            ft.Text("Cart: 0 items", size=14, weight="bold"),
            ft.ElevatedButton(
                "View Cart",
                on_click=lambda _: navigate_to(page, "user_cart", email, restaurant_id),
                icon=ft.icons.SHOPPING_CART
            )
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    def update_cart_display():
        total_items = sum(cart.values())
        if total_items > 0:
            cart_summary.controls[0].value = f"Cart: {total_items} items"
            cart_summary.visible = True
        else:
            cart_summary.visible = False
        page.update()

    def load_menu(user_type) -> ft.Column:
        try:
            supplier_menu = get_supplier_menu_with_dynamic_pricing(restaurant_id, user_type)
            if not supplier_menu:
                return ft.Column([ft.Text("Restaurant menu not available", color="red")])

            # User type badge
            user_badge = None
            if user_type == "StudentU":
                user_badge = ft.Container(
                    content=ft.Text("STUDENT (60% OFF)", size=12, color="white"),
                    bgcolor=ft.colors.BLUE,
                    padding=ft.padding.symmetric(horizontal=8, vertical=2),
                    border_radius=5
                )
            elif user_type == "BPLU":
                user_badge = ft.Container(
                    content=ft.Text("BPL (70% OFF)", size=12, color="white"),
                    bgcolor=ft.colors.GREEN,
                    padding=ft.padding.symmetric(horizontal=8, vertical=2),
                    border_radius=5
                )
            elif user_type == "NGO Employee":
                user_badge = ft.Container(
                    content=ft.Text("NGO (50% OFF)", size=12, color="white"),
                    bgcolor=ft.colors.ORANGE,
                    padding=ft.padding.symmetric(horizontal=8, vertical=2),
                    border_radius=5
                )

            header_controls = [
                ft.Text(supplier_menu['name'], size=24, weight="bold"),
                ft.Row([
                    ft.Icon(ft.icons.STAR, color="yellow", size=16),
                    ft.Text(f"{supplier_menu['rating']:.1f}"  if supplier_menu['rating'] is not None else "N/A", size=14),
                    ft.Icon(ft.icons.LOCATION_ON, size=16),
                    ft.Text(supplier_menu['location'], size=14),
                ], spacing=10),
                ft.Text(supplier_menu['contact'], size=14),
                ft.Text(
                    supplier_menu['description'] if supplier_menu['description'] else "",
                    size=12,
                    italic=True
                )
            ]

            if user_badge:
                header_controls.append(user_badge)

            header_controls.append(ft.Divider())

            # Create menu items list
            menu_list = ft.ListView(
                spacing=10,
                expand=True,
                padding=10
            )

            for item in supplier_menu['menu']:
                card = create_menu_item_card(item, cart, page, update_cart_display)
                menu_list.controls.append(card)

            if not menu_list.controls:
                menu_list.controls.append(ft.Text("No available items at this time", color="gray"))

            return ft.Column([
                ft.Container(
                    content=ft.Column(header_controls, spacing=10),
                    padding=20
                ),
                ft.Text("Available Items", size=18, weight="bold"),
                menu_list
            ], expand=True)

        except Exception as e:
            print(f"Error in load_menu: {e}")
            return ft.Column([
                ft.Text("Error loading menu", color="red", size=20),
                ft.Text(str(e), size=14)
            ])

    # Build the complete layout
    content = ft.Column(
        controls=[
            cart_summary,
            load_menu(user_type),
            ft.Row([
                ft.ElevatedButton(
                    "Back to Restaurants",
                    on_click=lambda _: navigate_to(page, "user_home", email),
                    icon=ft.icons.ARROW_BACK
                ),
            ], alignment=ft.MainAxisAlignment.CENTER)
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )

    # Initialize cart display
    update_cart_display()
    return content


def user_menu_fs(page: ft.Page, navigate_to, email, restaurant_id: int) -> ft.Container:
    """Entry point for the menu page"""
    page.title = "Restaurant Menu"
    page.bgcolor = "#FFF3E0"
    page.horizontal_alignment = "center"
    user_type = get_user_type(email)

    try:
        if not restaurant_id:
            raise ValueError("Restaurant ID is required")

        content = user_menu_page(page, navigate_to, email, restaurant_id, user_type)
        if not content:
            raise ValueError("Failed to create menu content")

        return ft.Container(
            content=content,
            padding=20,
            expand=True
        )

    except Exception as e:
        print(f"Error in user_menu_fs: {e}")
        return ft.Container(
            content=ft.Column([
                ft.Text("Error loading menu", size=20, color="red"),
                ft.Text(str(e), size=14),
                ft.ElevatedButton(
                    "Back to Restaurants",
                    on_click=lambda _: navigate_to(page, "user_home", email)
                )
            ], alignment=ft.MainAxisAlignment.CENTER),
            expand=True
        )