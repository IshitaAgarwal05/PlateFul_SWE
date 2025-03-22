import flet as ft

def home_page(page: ft.Page):
    page.title = "Food Ordering App"
    page.bgcolor = "#ffffff"

    # Search Bar
    search_bar = ft.TextField(
        hint_text="Restaurant name, cuisine, or a dish...",
        prefix_icon=ft.Icons.SEARCH,
        width=page.width * 0.9
    )

    # Filter Buttons
    filter_row = ft.Row(
        controls=[
            ft.ElevatedButton("Safe", bgcolor="gray200", color="black"),
            ft.ElevatedButton("₹₹", bgcolor="gray200", color="black"),
            ft.ElevatedButton("Cuisines", bgcolor="gray200", color="black"),
            ft.ElevatedButton("Popular", bgcolor="gray200", color="black")
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10
    )

    # Promotions
    promotions = ft.Row(
        controls=[
            ft.Container(
                content=ft.Text("60% OFF\nNew Cooking!", size=14, weight="bold", color="black"),
                bgcolor="red600", padding=20, border_radius=10, width=150
            ),
            ft.Container(
                content=ft.Text("Big Discounts", size=14, weight="bold", color="black"),
                bgcolor="blue600", padding=20, border_radius=10, width=150
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10
    )

    # Food Categories
    food_categories = ft.Row(
        controls=[
            ft.Column([ft.CircleAvatar(foreground_image_src="https://source.unsplash.com/50x50/?pizza"), ft.Text("Pizza", color="black")]),
            ft.Column([ft.CircleAvatar(foreground_image_src="https://source.unsplash.com/50x50/?burger"), ft.Text("Burger", color="black")]),
            ft.Column([ft.CircleAvatar(foreground_image_src="https://source.unsplash.com/50x50/?cake"), ft.Text("Cake", color="black")]),
            ft.Column([ft.CircleAvatar(foreground_image_src="https://source.unsplash.com/50x50/?sushi"), ft.Text("Sushi", color="black")]),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )

    # Restaurant Cards
    restaurant_data = [
        {"name": "Eat Healthy", "image": "https://source.unsplash.com/300x200/?healthyfood", "rating": "4.5", "time": "30 min"},
        {"name": "Aruat", "image": "https://source.unsplash.com/300x200/?dessert", "rating": "4.7", "time": "25 min"},
        {"name": "Tinka Fast Food", "image": "https://source.unsplash.com/300x200/?pasta", "rating": "4.3", "time": "20 min"},
        {"name": "Housemate Sweets", "image": "https://source.unsplash.com/300x200/?bakery", "rating": "4.6", "time": "35 min"},
    ]

    restaurant_list = ft.Column(
        controls=[
            ft.Card(
                content=ft.Row(
                    controls=[
                        ft.Image(src=item["image"], width=100, height=80, border_radius=10),
                        ft.Column([
                            ft.Text(item["name"], size=16, weight="bold", color="black"),
                            ft.Row([
                                ft.Icon(ft.Icons.STAR, color="yellow", size=14),
                                ft.Text(item["rating"], size=14, color="black")
                            ]),
                            ft.Text(f"Delivery in {item['time']}", size=12, color="gray")
                        ], spacing=5)
                    ]
                ), width=page.width * 0.9
            ) for item in restaurant_data
        ],
        spacing=10
    )

    # Bottom Navigation Bar
    bottom_nav = ft.BottomAppBar(
        bgcolor="white",
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            controls=[
                ft.IconButton(ft.Icons.HOME, on_click=lambda e: page.snack_bar(ft.SnackBar(ft.Text("Home Clicked")))),
                ft.IconButton(ft.Icons.FAVORITE_BORDER),
                ft.IconButton(ft.Icons.RECEIPT_LONG),
                ft.IconButton(ft.Icons.PERSON)
            ]
        )
    )

    # Adding Components to Page (with scrollable view)
    page.add(
        ft.ListView(
            controls=[
                ft.Text("Home", size=20, weight="bold", color="black"),
                search_bar,
                filter_row,
                promotions,
                ft.Text("Eat what makes you happy", size=16, weight="bold", color="black"),
                food_categories,
                ft.Text("Nearby Restaurants", size=16, weight="bold", color="black"),
                restaurant_list
            ],
            expand=True,  # To enable scrolling without scrollbars
            spacing=15
        )
    )

    # Add bottom nav separately so it doesn't scroll away
    page.add(bottom_nav)