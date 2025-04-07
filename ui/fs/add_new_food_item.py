import flet as ft
import sqlite3
import os
import shutil
from uuid import uuid4
from pathlib import Path


def save_food_item(restaurant_id, name, price, description, image_path):
    conn = sqlite3.connect("plateful.db")
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO FOOD_ITEM (restaurant_id, name, price, description, available) VALUES (?, ?, ?, ?, ?)",
            (restaurant_id, name, price, description, 1)
        )
        item_id = cursor.lastrowid
        conn.commit()

        if image_path and os.path.exists(image_path):
            # Create target directory if it doesn't exist
            target_dir = Path("assets/images/fs")
            target_dir.mkdir(parents=True, exist_ok=True)

            # Move the file to permanent location
            target_path = target_dir / f"{item_id}.png"
            shutil.move(image_path, target_path)

        return item_id

    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def get_supplier_id(email):
    conn = sqlite3.connect("plateful.db")
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT restaurant_id FROM FOOD_SUPPLIER WHERE email=?", (email,))
        result = cursor.fetchone()
        return result[0] if result else None
    finally:
        conn.close()


def add_food_item_page(page: ft.Page, navigate_to, email):
    def on_submit(e):
        if not new_item_name.value:
            page.snack_bar = ft.SnackBar(ft.Text("Item name is required!"))
            page.snack_bar.open = True
            page.update()
            return

        try:
            price = float(new_item_price.value) if new_item_price.value else 0.0
            save_food_item(
                supplier_id,
                new_item_name.value,
                price,
                new_item_description.value,
                temp_image_path
            )
            page.snack_bar = ft.SnackBar(ft.Text("Item added successfully!"))
            page.snack_bar.open = True
            page.update()
            navigate_to(page, "fs_desc", email)
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("Please enter a valid price!"))
            page.snack_bar.open = True
            page.update()
        except Exception as e:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {str(e)}"))
            page.snack_bar.open = True
            page.update()

    def on_cancel(e):
        navigate_to(page, "fs_desc", email)

    def on_pick_file(e: ft.FilePickerResultEvent):
        nonlocal temp_image_path
        if e.files:
            try:
                # Create temp directory if it doesn't exist
                temp_dir = Path("assets/images/temp")
                temp_dir.mkdir(parents=True, exist_ok=True)

                # Generate unique filename
                temp_path = temp_dir / f"temp_{uuid4()}.png"

                # Get the actual file path and copy it
                src_path = Path(e.files[0].path)
                shutil.copy(src_path, temp_path)

                temp_image_path = str(temp_path)
                selected_image.value = e.files[0].name
                selected_image.update()

                print(f"Image saved to: {temp_image_path}")

            except Exception as e:
                print(f"Error saving image: {e}")
                page.snack_bar = ft.SnackBar(
                    ft.Text(f"Error saving image: {str(e)}"),
                    bgcolor=ft.colors.RED
                )
                page.snack_bar.open = True
                page.update()

    supplier_id = get_supplier_id(email)
    if supplier_id is None:
        return ft.Text("Error: Supplier not found", color="red")

    # Initialize file picker
    file_picker = ft.FilePicker(on_result=on_pick_file)
    page.overlay.append(file_picker)
    page.update()

    temp_image_path = None
    new_item_name = ft.TextField(label="Item Name", autofocus=True)
    new_item_price = ft.TextField(label="Price", keyboard_type=ft.KeyboardType.NUMBER)
    new_item_description = ft.TextField(label="Description", multiline=True)
    selected_image = ft.Text("No image selected", italic=True)

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Add New Food Item", size=24, weight="bold"),
                new_item_name,
                new_item_price,
                new_item_description,
                ft.Row([
                    ft.ElevatedButton(
                        "Select Image",
                        icon=ft.icons.IMAGE,
                        on_click=lambda _: file_picker.pick_files(
                            allowed_extensions=["png", "jpg", "jpeg"],
                            dialog_title="Select food image",
                            allow_multiple=False
                        )
                    ),
                    selected_image
                ]),
                ft.Row([
                    ft.ElevatedButton(
                        "Cancel",
                        color="white",
                        bgcolor="#FF5252",
                        on_click=on_cancel
                    ),
                    ft.ElevatedButton(
                        "Save",
                        color="white",
                        bgcolor="#4CAF50",
                        on_click=on_submit
                    )
                ], alignment="end")
            ],
            spacing=20,
            scroll=True,
            expand=True
        ),
        padding=20,
        expand=True
    )


def add_new_food(page: ft.Page, navigate_to, email):
    page.title = "Add New Food Item"
    page.bgcolor = "#FFF3E0"
    page.horizontal_alignment = "center"

    try:
        content = add_food_item_page(page, navigate_to, email)
        page.clean()
        page.add(content)
        page.update()
    except Exception as e:
        page.clean()
        page.add(ft.Text(f"Failed to load page: {str(e)}", color="red"))
        page.update()