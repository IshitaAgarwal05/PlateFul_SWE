import flet as ft
import sqlite3


def supplier_insights(page: ft.Page, navigate_to, email):
    try:
        conn = sqlite3.connect("plateful.db")
        cursor = conn.cursor()

        # Get supplier by email
        cursor.execute("SELECT restaurant_id, location, name FROM FOOD_SUPPLIER WHERE email=?", (email,))
        supplier = cursor.fetchone()

        if not supplier:
            conn.close()
            return ft.Text("Supplier not found", color="red", size=20)

        restaurant_id, location, supplier_name = supplier

        # Get description
        cursor.execute("SELECT description FROM FOOD_SUPPLIER WHERE name=?", (supplier_name,))
        supplier_desc = cursor.fetchone()
        description = supplier_desc[0] if supplier_desc else "No description"

        # Order data
        def fetch_order_data(status):
            with sqlite3.connect("plateful.db") as temp_conn:
                temp_cursor = temp_conn.cursor()
                temp_cursor.execute("""
                    SELECT SUM(total_amount), COUNT(*)
                    FROM "ORDER"
                    WHERE restaurant_id=? AND status=?
                """, (restaurant_id, status))
                return temp_cursor.fetchone() or (0, 0)

        accepted_amount, accepted_orders = fetch_order_data("Accepted")
        rejected_amount, rejected_orders = fetch_order_data("Rejected")

        # Editable description
        description_field = ft.TextField(
            value=description,
            multiline=True,
            width=500,
            label="Supplier Description"
        )

        def update_description(e):
            new_desc = description_field.value.strip()
            if new_desc:
                with sqlite3.connect("plateful.db") as temp_conn:
                    temp_cursor = temp_conn.cursor()
                    temp_cursor.execute(
                        "UPDATE FOOD_SUPPLIER SET description=? WHERE name=?",
                        (new_desc, supplier_name)
                    )
                    temp_conn.commit()
                page.snack_bar = ft.SnackBar(ft.Text("Description updated successfully!"))
                page.snack_bar.open = True
                page.update()

        # Back button
        back_button = ft.IconButton(
            icon=ft.icons.ARROW_BACK,
            icon_color=ft.colors.BLUE,
            on_click=lambda _: navigate_to(page, "fs_desc", email),
            tooltip="Back to Supplier Dashboard"
        )

        # Build UI
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    back_button,
                    ft.Text("Supplier Insights", size=20, weight="bold"),
                ], alignment=ft.MainAxisAlignment.START),
                ft.Divider(),
                ft.Text(supplier_name, weight=ft.FontWeight.BOLD, size=24),
                description_field,
                ft.ElevatedButton(
                    "Update Description",
                    on_click=update_description,
                    icon=ft.icons.UPDATE
                ),
                ft.Text(f"Location: {location}", size=14, italic=True),
                ft.Divider(),
                ft.Text("Accepted Orders", weight=ft.FontWeight.BOLD, size=18),
                ft.Text(f"Total: ₹{accepted_amount} | Orders: {accepted_orders}"),
                ft.Divider(),
                ft.Text("Rejected Orders", weight=ft.FontWeight.BOLD, size=18),
                ft.Text(f"Total: ₹{rejected_amount} | Orders: {rejected_orders}"),
            ],
                spacing=20,
                scroll=ft.ScrollMode.AUTO)
        )

    except Exception as e:
        return ft.Column([
            ft.Text(f"Error: {str(e)}", color="red", size=20),
            ft.ElevatedButton(
                "Back to Dashboard",
                on_click=lambda _: navigate_to(page, "fs_desc", email)
            )
        ])

    finally:
        if 'conn' in locals() and conn:
            conn.close()