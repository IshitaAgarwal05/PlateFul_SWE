import flet as ft
import sqlite3
from typing import Optional, List, Dict
from db.models import get_user_type


# Database Helper Functions
def get_user_location(email: str) -> Optional[str]:
    """Get the user's location from USER table"""
    conn = sqlite3.connect('plateful.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT location FROM USER WHERE email=?", (email,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"Error getting user location: {e}")
        return None
    finally:
        conn.close()


def get_food_suppliers(location: str) -> List[Dict]:
    """Get active food suppliers in a specific location"""
    conn = sqlite3.connect('plateful.db')
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT restaurant_id, name, location, rating, description FROM FOOD_SUPPLIER "
            "WHERE location=? AND is_active=1",
            (location,)
        )
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except Exception as e:
        print(f"Error getting food suppliers: {e}")
        return []
    finally:
        conn.close()


# Main Page Function
def home_page(page: ft.Page, navigate_to, email):
    # Get user's location
    user_location = get_user_location(email)
    if not user_location:
        return ft.Text("Could not determine your location. Please update your profile.", color="red")

    # Get food suppliers in the same location
    food_suppliers = get_food_suppliers(user_location)

    # Create main container
    scrollable_content = ft.Column(spacing=15, expand=True, scroll=ft.ScrollMode.AUTO)

    # Modified navigation handler that accepts restaurant_id
    def navigate_to_menu(e, restaurant_id=None):
        navigate_to(page, "user_menu_fs", email, restaurant_id)

    def navigate_to_profile(e):
        try:
            user_type = get_user_type(email)
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

    def show_snackbar(message):
        page.snack_bar = ft.SnackBar(ft.Text(message), bgcolor=ft.colors.RED)
        page.snack_bar.open = True
        page.update()

    # Search Bar
    search_bar = ft.TextField(
        hint_text=f"Search in {user_location}...",
        prefix_icon=ft.icons.SEARCH,
        width=page.width * 0.9,
        border_radius=10,
        border_color=ft.colors.GREY_300,
        filled=True,
        fill_color=ft.colors.WHITE,
        on_submit=lambda e: filter_suppliers(e.control.value)
    )

    def filter_suppliers(search_term: str):
        filtered = [s for s in food_suppliers
                   if search_term.lower() in s['name'].lower() or
                   (s['description'] and search_term.lower() in s['description'].lower())]
        update_restaurant_list(filtered)

    def safe_compare_rating(rating, threshold=4):
        """Safely compare ratings that might be None"""
        if rating is None:
            return False
        try:
            return float(rating) >= threshold
        except (ValueError, TypeError):
            return False

    def get_safe_rating(supplier):
        """Get rating with None handling"""
        rating = supplier.get('rating')
        if rating is None:
            return 0
        try:
            return float(rating)
        except (ValueError, TypeError):
            return 0

    def update_restaurant_list(suppliers: List[Dict]):
        restaurant_list.controls.clear()

        if not suppliers:
            restaurant_list.controls.append(
                ft.Text("No matching restaurants found", color="gray")
            )
        else:
            for supplier in suppliers:
                card = create_restaurant_card(supplier)
                restaurant_list.controls.append(card)

        page.update()

    def create_restaurant_card(supplier: Dict) -> ft.GestureDetector:
        rating = get_safe_rating(supplier)
        rating_display = f"{rating:.1f}" if rating is not None else "N/A"

        card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Image(
                            src=supplier.get('image_url', 'https://source.unsplash.com/300x200/?restaurant'),
                            width=120,
                            height=90,
                            border_radius=10,
                            fit=ft.ImageFit.COVER,
                            expand=True
                        ),
                        ft.Column([
                            ft.Text(supplier['name'], size=16, weight="bold"),
                            ft.Row([
                                ft.Icon(ft.icons.STAR, color="yellow", size=14),
                                ft.Text(rating_display),
                                ft.Text("•"),
                                ft.Text(supplier['location'], size=12)
                            ], spacing=5),
                            ft.Text(
                                supplier.get('description', '')[:60] + '...' if supplier.get('description') else '',
                                size=12,
                                color=ft.colors.GREY
                            )
                        ], spacing=5, expand=True)
                    ], spacing=10),
                    ft.Divider(height=1)
                ], spacing=5),
                padding=10,
                width=page.width * 0.95
            ),
            elevation=2,
            margin=ft.margin.symmetric(vertical=5)
        )

        return ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.CLICK,
            on_tap=lambda e, s=supplier: navigate_to_menu(e, restaurant_id=s['restaurant_id']),
            content=card
        )

    # Filter Buttons with safe rating comparison
    filter_row = ft.Row(
        controls=[
            ft.ElevatedButton("All", on_click=lambda e: update_restaurant_list(food_suppliers)),
            ft.ElevatedButton("⭐ 4+", on_click=lambda e: update_restaurant_list(
                [s for s in food_suppliers if safe_compare_rating(s.get('rating'))])),
            ft.ElevatedButton("Popular", on_click=lambda e: update_restaurant_list(
                sorted(food_suppliers, key=lambda x: get_safe_rating(x), reverse=True))),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
        scroll=ft.ScrollMode.AUTO
    )

    # Restaurant List
    restaurant_list = ft.Column(spacing=5)
    update_restaurant_list(food_suppliers)

    # Bottom Navigation Bar
    bottom_nav = ft.Container(
        content=ft.BottomAppBar(
            bgcolor="white",
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                controls=[
                    ft.IconButton(icon=ft.icons.HOME, icon_color=ft.colors.BLUE),
                    ft.IconButton(icon=ft.icons.SEARCH),
                    ft.IconButton(icon=ft.icons.FAVORITE_BORDER),
                    ft.IconButton(
                        icon=ft.icons.PERSON,
                        on_click=navigate_to_profile
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

    # Header with location
    location_header = ft.Row(
        controls=[
            ft.Icon(ft.icons.LOCATION_ON, color=ft.colors.BLUE, size=20),
            ft.Text(user_location, weight="bold"),
            ft.Icon(ft.icons.ARROW_DROP_DOWN)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=5
    )

    # Assemble all components
    scrollable_content.controls.extend([
        ft.Container(height=10),
        location_header,
        ft.Container(height=10),
        search_bar,
        ft.Container(height=15),
        filter_row,
        ft.Container(height=15),
        ft.Text("Available Restaurants", size=18, weight="bold"),
        restaurant_list,
        ft.Container(height=80)  # Space for bottom nav
    ])

    # Final layout
    layout = ft.Stack(
        controls=[
            scrollable_content,
            bottom_nav
        ],
        expand=True
    )

    return layout