import flet as ft
import sqlite3


def get_supplier_data(email):
    conn = sqlite3.connect("plateful.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM FOOD_SUPPLIER WHERE email=?", (email,))
    restaurant = cursor.fetchone()

    if not restaurant:
        conn.close()
        return None, []

    cursor.execute("SELECT * FROM FOOD_ITEM WHERE restaurant_id=?", (restaurant[0],))
    menu_items = cursor.fetchall()

    conn.close()
    return restaurant, menu_items


def food_supplier_page(page, email):
    restaurant, menu_items = get_supplier_data(email)

    if not restaurant:
        return ft.Text("❌ No supplier found for this email.")

    name, location, contact, rating, description = restaurant[1], restaurant[2], restaurant[3], restaurant[5], \
    restaurant[7]

    header = ft.Container(
        content=ft.Column([
            ft.Text(name, size=24, weight="bold", color="white"),
            ft.Text(f"{location}", color="white"),
            ft.Row([
                ft.Text(f"⭐ {rating}/5", color="white"),
                ft.Text(f"📞 {contact}", color="white"),
            ])
        ]),
        padding=20,
        bgcolor="#FF7043",
        border_radius=ft.border_radius.only(top_left=20, top_right=20)
    )

    menu_list = []
    if not menu_items:
        menu_list.append(ft.Text("⚠️ No menu items available."))
    else:
        for item in menu_items:
            item_id, _, item_name, price, desc, available = item
            status_color = "green" if available else "red"
            menu_list.append(
                ft.Container(
                    content=ft.Row([
                        ft.Image(src=f"/images/{item_id}.png", width=60, height=60),
                        ft.Column([
                            ft.Text(item_name, size=18, weight="bold", color="black"),
                            ft.Text(f"₹{price}", weight="bold", color="black"),
                            ft.Text(desc, color="black"),
                        ], spacing=2),
                        ft.Switch(value=available, active_color=status_color),
                    ], alignment="spaceBetween"),
                    padding=10,
                    border=ft.border.all(1, "#E0E0E0"),
                    border_radius=10,
                    margin=5
                )
            )

    return ft.Column([
        header,
        ft.Row([
            ft.TextField(label="Search", expand=True),
            ft.IconButton(ft.icons.SEARCH)
        ], alignment="center"),
        ft.ListView(menu_list, expand=True)
    ])


def desc(page):
    page.title = "Food Supplier Menu"
    page.bgcolor = "#FFF3E0"
    page.add(food_supplier_page(page, email="00001"))
    page.update()
