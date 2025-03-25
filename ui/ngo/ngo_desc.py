import flet as ft
import sqlite3


# Function to fetch NGO details based on the logged-in email
def get_ngo_details(email):
    conn = sqlite3.connect("plateful.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM NGO WHERE email = ?", (email,))
    ngo = cursor.fetchone()

    conn.close()

    if ngo:
        ngo_details = {
            "name": ngo[1],
            "location": ngo[2],
            "contact": ngo[3],
            "email": ngo[4],
            "description": ngo[6],
        }
        return ngo_details
    return None


# Function to build the UI
def desc(page: ft.Page):
    page.title = "NGO Team Details"
    page.bgcolor = "#FF6F4F"

    # Simulating a logged-in user's email
    logged_in_email = "001"

    # Fetch NGO details
    ngo_details = get_ngo_details(logged_in_email)

    if not ngo_details:
        page.controls.append(ft.Text("NGO details not found!", size=20, color="white"))
        return

    # Header
    header = ft.Row(
        [
            ft.IconButton(icon=ft.icons.ARROW_BACK, icon_color="white"),
            ft.Text("Team Details", size=20, color="white", weight=ft.FontWeight.BOLD),
            ft.IconButton(icon=ft.icons.EDIT, icon_color="white"),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    # NGO Details Section
    ngo_card = ft.Container(
        content=ft.Column(
            [
                ft.Text(ngo_details["name"], size=22, weight=ft.FontWeight.BOLD),
                ft.Text(ngo_details["description"], size=14),
                ft.Text(f"Address: {ngo_details['location']}", size=14, italic=True),
                ft.Text(f"Contact: {ngo_details['contact']}", size=14),
                ft.Text(f"Email: {ngo_details['email']}", size=14),
            ],
            spacing=5,
        ),
        padding=15,
        bgcolor="white",
        border_radius=10,
    )

    # Assigned Team Members (Placeholder for now)
    assigned_section = ft.Container(
        content=ft.Column(
            [
                ft.Text("Assigned to", size=18, weight=ft.FontWeight.BOLD),
                ft.Row([ft.CircleAvatar(content=ft.Text("A")), ft.CircleAvatar(content=ft.Text("B")),
                        ft.CircleAvatar(content=ft.Text("+"))]),
            ]
        ),
        padding=15,
        bgcolor="white",
        border_radius=10,
    )

    # Past Orders (Placeholder)
    past_orders_section = ft.Container(
        content=ft.Column(
            [
                ft.Text("Past Orders", size=18, weight=ft.FontWeight.BOLD),
                ft.ListTile(title=ft.Text("SMI CAFE"), subtitle=ft.Text("11 May 2:44pm"),
                            leading=ft.Icon(ft.icons.CHECK_CIRCLE, color="blue")),
                ft.ListTile(title=ft.Text("My Village Restaurant"), subtitle=ft.Text("18 Dec 1:04pm"),
                            leading=ft.Icon(ft.icons.CHECK_CIRCLE, color="blue")),
                ft.ListTile(title=ft.Text("Jaipur Restaurant"), subtitle=ft.Text("01 Feb 1:40pm"),
                            leading=ft.Icon(ft.icons.CIRCLE_OUTLINED)),
                ft.ListTile(title=ft.Text("House of Tandoor"), subtitle=ft.Text("01 Sep 2:40pm"),
                            leading=ft.Icon(ft.icons.CIRCLE_OUTLINED)),
            ]
        ),
        padding=15,
        bgcolor="white",
        border_radius=10,
    )

    # Adding all elements to the page
    page.add(header, ngo_card, assigned_section, past_orders_section)
