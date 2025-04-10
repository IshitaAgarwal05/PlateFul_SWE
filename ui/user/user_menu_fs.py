import flet as ft
import sqlite3
from typing import Optional, Dict, List

# Global variable to store cart items
user_carts = {}


def get_supplier_menu(restaurant_id: int) -> Optional[Dict]:
    """Get food supplier menu with only available items"""
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
            "SELECT item_id, name, price, description FROM FOOD_ITEM "
            "WHERE restaurant_id = ? AND available = 1",
            (restaurant_id,)
        )
        menu_items = cursor.fetchall()

        return {
            "restaurant_id": restaurant_id,
            "name": supplier_data[0],
            "location": supplier_data[1],
            "contact": supplier_data[2],
            "rating": supplier_data[3],
            "description": supplier_data[4],
            "menu": [
                {
                    "item_id": item[0],
                    "name": item[1],
                    "price": item[2],
                    "description": item[3]
                }
                for item in menu_items
            ]
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

    def update_quantity(increment):
        new_quantity = max(0, quantity + increment)
        if new_quantity == 0:
            cart.pop(item['item_id'], None)
        else:
            cart[item['item_id']] = new_quantity
        quantity_text.value = str(new_quantity)
        page.update()
        update_cart_fn()

    return ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Image(
                        src=f"/images/fs/{item['item_id']}.png",
                        width=100,
                        height=80,
                        border_radius=10,
                        fit=ft.ImageFit.COVER,
                        error_content=ft.Icon(ft.icons.FASTFOOD, size=50)
                    ),
                    ft.Column([
                        ft.Text(item['name'], size=16, weight="bold"),
                        ft.Text(f"₹{item['price']:.2f}", size=14),
                        ft.Text(
                            item['description'] if item['description'] else "No description available",
                            size=12,
                            color=ft.colors.GREY_600
                        )
                    ], spacing=5, expand=True),
                    ft.Row([
                        ft.IconButton(
                            ft.icons.REMOVE,
                            on_click=lambda e: update_quantity(-1),
                            icon_size=20
                        ),
                        quantity_text,
                        ft.IconButton(
                            ft.icons.ADD,
                            on_click=lambda e: update_quantity(1),
                            icon_size=20
                        ),
                    ], spacing=0)
                ], spacing=15)
            ]),
            padding=15,
            width=400
        ),
        elevation=3,
        margin=10
    )


def user_menu_page(page: ft.Page, navigate_to, email, restaurant_id: int) -> ft.Column:
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
                on_click=lambda _: navigate_to(page, "user_cart", email),
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

    def load_menu() -> ft.Column:
        supplier_menu = get_supplier_menu(restaurant_id)
        if not supplier_menu:
            return ft.Column([ft.Text("Restaurant menu not available", color="red")])

        header = ft.Container(
            content=ft.Column([
                ft.Text(supplier_menu['name'], size=24, weight="bold"),
                ft.Row([
                    ft.Icon(ft.icons.STAR, color="yellow", size=16),
                    ft.Text(str(supplier_menu['rating']), size=14),
                    ft.Icon(ft.icons.LOCATION_ON, size=16),
                    ft.Text(supplier_menu['location'], size=14),
                ], spacing=10),
                ft.Text(supplier_menu['contact'], size=14),
                ft.Text(
                    supplier_menu['description'] if supplier_menu['description'] else "",
                    size=12,
                    italic=True
                ),
                ft.Divider()
            ], spacing=10),
            padding=20
        )

        menu_items = ft.Column(
            controls=[create_menu_item_card(item, cart, page, update_cart_display)
                      for item in supplier_menu['menu']],
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )

        if not supplier_menu['menu']:
            menu_items.controls.append(
                ft.Text("No available items at this time", color="gray")
            )

        return ft.Column([
            header,
            ft.Text("Available Items", size=18, weight="bold"),
            menu_items
        ], expand=True)

    # Build the complete layout
    content = ft.Column(
        controls=[
            cart_summary,
            load_menu(),
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

    # Initialize cart display after all controls are created
    update_cart_display()

    return content


def user_menu_fs(page: ft.Page, navigate_to, email, restaurant_id: int) -> ft.Container:
    """Entry point for the menu page"""
    page.title = "Restaurant Menu"
    page.bgcolor = "#FFF3E0"
    page.horizontal_alignment = "center"

    try:
        if not restaurant_id:
            raise ValueError("Restaurant ID is required")

        content = user_menu_page(page, navigate_to, email, restaurant_id)
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