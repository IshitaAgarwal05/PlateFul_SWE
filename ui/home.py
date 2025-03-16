import flet as ft
from db.models import *

def home_page(page: ft.Page):
    page.title = "Plateful - Home"

    title_field = ft.TextField(label="Recipe Title")
    ingredients_field = ft.TextField(label="Ingredients")
    steps_field = ft.TextField(label="Steps")
    recipe_list = ft.Column()

    def load_recipes():
        recipe_list.controls.clear()
        for recipe in get_recipes():
            recipe_card = ft.Card(
                content=ft.Container(
                    ft.Column([
                        ft.Text(f"{recipe[1]}", size=20, weight="bold"),
                        ft.Text(f"Ingredients: {recipe[2]}"),
                        ft.Text(f"Steps: {recipe[3]}"),
                        ft.ElevatedButton(
                            "Delete",
                            on_click=lambda e, recipe_id=recipe[0]: handle_delete_recipe(recipe_id)
                        )
                    ])
                )
            )
            recipe_list.controls.append(recipe_card)
        page.update()

    def handle_add_recipe(e):
        add_recipe(title_field.value, ingredients_field.value, steps_field.value)
        load_recipes()

    def handle_delete_recipe(recipe_id):
        delete_recipe(recipe_id)
        load_recipes()

    load_recipes()

    return ft.Column([
        ft.Text("Welcome to Plateful!", size=30, weight="bold"),
        title_field,
        ingredients_field,
        steps_field,
        ft.ElevatedButton("Add Recipe", on_click=handle_add_recipe),
        recipe_list
    ])


