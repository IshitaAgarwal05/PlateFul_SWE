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


def food_supplier_page(page, navigate_to, email):
    def update_availability(item_id, value):
        conn = sqlite3.connect("plateful.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE FOOD_ITEM SET available=? WHERE item_id=?", (1 if value else 0, item_id))
        conn.commit()
        conn.close()

    try:
        restaurant, menu_items = get_supplier_data(email)

        if not restaurant:
            return ft.Text("❌ No supplier found for this email.", color="red", size=20)

        supplier_name, location, contact, rating, description = (
            restaurant[1], restaurant[2], restaurant[3], restaurant[5], restaurant[7]
        )

        # Create header content with description in the right position
        header_content = [
            ft.Text(supplier_name, size=24, weight="bold", color="white"),
        ]

        # Add description right after name if available
        if description and description.strip():
            header_content.append(
                ft.Text(description, color="white", size=14, italic=True)
            )

        # Add location and contact info
        header_content.extend([
            ft.Text(f"{location}", color="white"),
            ft.Row([
                ft.Text(f"⭐ {rating}/5", color="white"),
                ft.Text(f"📞 {contact}", color="white"),
            ]),
            ft.ElevatedButton(
                "View Supplier Insights",
                on_click=lambda _: navigate_to(page, "supplier_insights", email)
            )
        ])

        header = ft.Container(
            content=ft.Column(header_content, spacing=5),
            padding=20,
            bgcolor="#FF7043",
            border_radius=ft.border_radius.only(top_left=20, top_right=20)
        )

        # Build menu items
        menu_list = []
        if not menu_items:
            menu_list.append(ft.Text("⚠️ No menu items available."))
        else:
            for item in menu_items:
                item_id, _, item_name, price, desc, available = item
                status_color = "green" if available else "red"
                switch = ft.Switch(
                    value=bool(available),
                    active_color=status_color,
                    on_change=lambda e, item_id=item_id: update_availability(item_id, e.control.value)
                )
                menu_list.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Image(src=f"/images/{item_id}.png", width=60, height=60),
                            ft.Column([
                                ft.Text(item_name, size=18, weight="bold", color="black"),
                                ft.Text(f"₹{price:.2f}", weight="bold", color="black"),
                                ft.Text(desc, color="grey"),
                            ], spacing=5, expand=True),
                            switch,
                        ], alignment="center"),
                        padding=10,
                        border=ft.border.all(1, "#E0E0E0"),
                        border_radius=10,
                        margin=5,
                        bgcolor="#FFF7E0"
                    )
                )

        return ft.Column([
            header,
            ft.Container(
                content=ft.Row([
                    ft.TextField(label="Search", expand=True),
                    ft.IconButton(ft.icons.SEARCH)
                ], alignment="center"),
                padding=10,
            ),
            ft.ElevatedButton(
                "Add Food Item",
                on_click=lambda _: navigate_to(page, "add_new_food", email)
            ),
            ft.Column(
                menu_list,
                spacing=10,
                scroll=True,
                expand=True
            )
        ], expand=True)

    except Exception as e:
        print(f"Error in food_supplier_page: {e}")
        return ft.Text(f"Error loading page: {str(e)}", color="red", size=16)

def desc(page, navigate_to, email):
    page.title = "Food Supplier Menu"
    page.bgcolor = "#FFF3E0"

    try:
        content = food_supplier_page(page, navigate_to, email)
        if content is None:
            raise ValueError("food_supplier_page returned None")

        page.clean()
        page.add(content)
        page.update()

    except Exception as e:
        page.clean()
        page.add(ft.Text(f"Failed to load page: {str(e)}", color="red"))
        page.update()