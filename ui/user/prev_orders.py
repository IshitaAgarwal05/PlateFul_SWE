import flet as ft
import sqlite3
from typing import List, Dict
from datetime import datetime
from ui.user.home import wrap_with_nav


def get_previous_orders(email: str) -> List[Dict]:
    """Get previous orders for a user"""
    conn = sqlite3.connect('plateful.db')
    try:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT 
                o.order_id, 
                o.order_time, 
                o.total_amount,
                fs.name as restaurant_name,
                GROUP_CONCAT(fi.name || ' (' || oi.quantity || ')', ', ') as items
            FROM "ORDER" o
            JOIN FOOD_SUPPLIER fs ON o.restaurant_id = fs.restaurant_id
            JOIN ORDER_ITEM oi ON o.order_id = oi.order_id
            JOIN FOOD_ITEM fi ON oi.food_item_id = fi.item_id
            WHERE o.user_id = (SELECT user_id FROM USER WHERE email = ?)
            GROUP BY o.order_id
            ORDER BY o.order_time DESC""",
            (email,)
        )
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except Exception as e:
        print(f"Error getting previous orders: {e}")
        return []
    finally:
        conn.close()


def format_order_time(order_time: str) -> str:
    """Format database timestamp to readable format"""
    try:
        dt = datetime.strptime(order_time, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%b %d, %Y at %I:%M %p")
    except:
        return order_time


def create_order_card(order: Dict) -> ft.Card:
    """Create a card for an order"""
    return ft.Card(
        elevation=2,
        content=ft.Container(
            padding=10,
            content=ft.Column([
                ft.Row([
                    ft.Text(f"Order #{order['order_id']}", weight="bold"),
                    ft.Text(format_order_time(order['order_time']), size=12, color=ft.colors.GREY),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Text(order['restaurant_name'], size=14),
                ft.Text(order['items'], size=12, color=ft.colors.GREY_600),
                ft.Row([
                    ft.Text(f"₹{order['total_amount']:.2f}", weight="bold"),
                ], alignment=ft.MainAxisAlignment.END)
            ], spacing=5)
        )
    )



def previous_orders_page(page: ft.Page, navigate_to, email, navigate_to_profile):
    orders = get_previous_orders(email)

    if not orders:
        content = ft.Column([
            ft.Icon(ft.icons.HISTORY, size=48, color=ft.colors.GREY_400),
            ft.Text("No previous orders found", size=18),
            ft.Text("Your order history will appear here", size=14, color=ft.colors.GREY),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20, expand=True)
    else:
        content = ft.ListView(
            controls=[create_order_card(order) for order in orders],
            spacing=10,
            padding=20,
            expand=True
        )

    main_content = ft.Column([
        ft.Text("Your Orders", size=24, weight="bold"),
        ft.Divider(),
        content
    ], spacing=20)

    return wrap_with_nav(main_content, page, email, navigate_to, navigate_to_profile)


