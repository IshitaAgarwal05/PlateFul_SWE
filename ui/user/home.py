import flet as ft
from db.models import get_food_suppliers, get_user_type

def home_page(page: ft.Page, navigate_to, email):
    # Create a main container that will hold everything
    scrollable_content = ft.Column(spacing=15, expand=True, scroll=ft.ScrollMode.AUTO)

    # Function to handle profile navigation
    def navigate_to_profile(e):
        print("Profile button clicked!")
        try:
            print(f"Current email: {email}")
            user_type = get_user_type(email)
            print(f"Detected user type: {user_type}")
            if user_type == "NGO Employee":
                navigate_to(page, "ngo_desc", email)
            elif user_type in ["student_verification", "bpl_verification"]:
                navigate_to(page, "user_profile", email)
            elif user_type == "FS Employee":
                navigate_to(page, "fs_profile", email)
            else:
                show_snackbar(f"No profile page available for {user_type} users")
        except Exception as e:
            show_snackbar(f"Error navigating to profile: {str(e)}")

    # Helper function for snackbar
    def show_snackbar(message):
        page.snack_bar = ft.SnackBar(
            ft.Text(message),
            bgcolor=ft.colors.RED
        )
        page.snack_bar.open = True
        page.update()

    # Search Bar
    search_bar = ft.TextField(
        hint_text="Restaurant name, cuisine, or a dish...",
        prefix_icon=ft.icons.SEARCH,
        width=page.width * 0.9,
        border_radius=10,
        border_color=ft.colors.GREY_300,
        filled=True,
        fill_color=ft.colors.WHITE
    )

    # Search Bar Container (fixed at top)
    search_container = ft.Container(
        content=ft.Column([
            ft.Container(height=10),
            search_bar,
            ft.Container(height=10)
        ]),
        padding=ft.padding.symmetric(horizontal=20),
        top=0,
        left=0,
        right=10,
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
            ft.Column(
                [ft.CircleAvatar(foreground_image_src="https://source.unsplash.com/50x50/?pizza"),
                 ft.Text("Pizza", color="black")],
                spacing=5
            ),
            ft.Column(
                [ft.CircleAvatar(foreground_image_src="https://source.unsplash.com/50x50/?burger"),
                 ft.Text("Burger", color="black")],
                spacing=5
            ),
            ft.Column(
                [ft.CircleAvatar(foreground_image_src="https://source.unsplash.com/50x50/?cake"),
                 ft.Text("Cake", color="black")],
                spacing=5
            ),
            ft.Column(
                [ft.CircleAvatar(foreground_image_src="https://source.unsplash.com/50x50/?sushi"),
                 ft.Text("Sushi", color="black")],
                spacing=5
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )

    # Restaurant Cards
    restaurant_data = [
        {"name": "Eat Healthy", "image": "https://source.unsplash.com/300x200/?healthyfood", "rating": "4.5",
         "time": "30 min"},
        {"name": "Aruat", "image": "https://source.unsplash.com/300x200/?dessert", "rating": "4.7", "time": "25 min"},
        {"name": "Tinka Fast Food", "image": "https://source.unsplash.com/300x200/?pasta", "rating": "4.3",
         "time": "20 min"},
        {"name": "Housemate Sweets", "image": "https://source.unsplash.com/300x200/?bakery", "rating": "4.6",
         "time": "35 min"},
    ]

    # Create restaurant cards with proper lambda capture
    restaurant_list = ft.Column(spacing=10)
    for item in restaurant_data:
        card = ft.Card(
            content=ft.Row(
                controls=[
                    ft.Image(
                        src=item["image"],
                        width=100,
                        height=80,
                        border_radius=10,
                        fit=ft.ImageFit.COVER
                    ),
                    ft.Column([
                        ft.Text(item["name"], size=16, weight="bold", color="black"),
                        ft.Row([
                            ft.Icon(ft.icons.STAR, color="yellow", size=14),
                            ft.Text(item["rating"], size=14, color="black")
                        ]),
                        ft.Text(f"Delivery in {item['time']}", size=12, color="gray")
                    ], spacing=5)
                ],
                spacing=10
            ),
            width=page.width * 0.9
        )

        # Create gesture detector with proper lambda
        gesture = ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.CLICK,
            on_tap=lambda e, item=item: navigate_to(page, "menu", email),
            content=card
        )
        restaurant_list.controls.append(gesture)

    # Bottom Navigation Bar - Fixed to stay at bottom
    bottom_nav = ft.Container(
        content=ft.BottomAppBar(
            bgcolor="white",
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                controls=[
                    ft.IconButton(
                        icon=ft.icons.HOME,
                        on_click=lambda e: navigate_to(page, "home", email)
                    ),
                    ft.IconButton(icon=ft.icons.FAVORITE_BORDER),
                    ft.IconButton(icon=ft.icons.RECEIPT_LONG),
                    ft.IconButton(
                        icon=ft.icons.PERSON,
                        on_click=lambda e, nav=navigate_to, pg=page, em=email: navigate_to_profile(e)
                    )
                ]
            ),
            elevation=8
        ),
        bottom=0,
        left=0,
        right=0,
        padding=0
    )

    # Add all components to scrollable content
    scrollable_content.controls.extend([
        ft.Container(height=80),  # Space for search bar
        filter_row,
        promotions,
        food_categories,
        ft.Text("Nearby Restaurants", size=16, weight="bold", color="black"),
        restaurant_list,
        ft.Container(height=80)  # Space for bottom nav
    ])

    # Create the final layout with fixed elements
    layout = ft.Stack(
        controls=[
            scrollable_content,
            search_container,
            bottom_nav
        ],
        expand=True
    )

    return layout