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
        return {
            "ngo_id": ngo[0],
            "name": ngo[1],
            "location": ngo[2],
            "contact": ngo[3],
            "email": ngo[4],
            "description": ngo[6],
        }
    return None


# Function to build the UI
def desc(page: ft.Page, navigate_to, email):
    try:
        page.title = "NGO Details"
        page.bgcolor = "#FF6F4F"
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        # Fetch NGO details including ngo_id
        ngo_details = get_ngo_details(email)

        if not ngo_details:
            return ft.Text("NGO details not found!", size=20, color="white")

        # Extract ngo_id from the details
        ngo_id = ngo_details["ngo_id"]

        # Header
        header = ft.Row(
            [
                ft.IconButton(icon=ft.icons.ARROW_BACK, icon_color="white"),
                ft.Text("Team Details", size=20, color="white", weight=ft.FontWeight.BOLD),
                ft.IconButton(icon=ft.icons.EDIT, icon_color="white"),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            width=page.width
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
                    ft.Text(f"NGO ID: {ngo_id}", size=12, color="grey"),
                ],
                spacing=8,
                alignment=ft.CrossAxisAlignment.START
            ),
            padding=15,
            bgcolor="white",
            border_radius=10,
            width=page.width - 40,
            margin=ft.margin.symmetric(horizontal=20)
        )

        # Donation button
        donation_button = ft.ElevatedButton(
            "Receive Donations",
            icon=ft.icons.ATTACH_MONEY,
            on_click=lambda _: navigate_to(page, "ngo_donation", ngo_id),
            expand=True,
            height=50,
        )

        # View Donations button
        view_donation_button = ft.ElevatedButton(
            "View Donations",
            icon=ft.icons.HISTORY,
            on_click=lambda _: navigate_to(page, "ngo_donations_view", ngo_id),
            expand=True,
            height=50,
        )

        # View Donations button
        order_button = ft.ElevatedButton(
            "Order",
            icon=ft.icons.SHOPPING_CART,
            on_click=lambda _: navigate_to(page, "ngo_home", email),
            expand=True,
            height=50,
        )

        # Button container for better layout
        button_row = ft.Container(
            content=ft.Column(
                [
                    donation_button,
                    view_donation_button,
                    order_button
                ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                spacing=10,
                width=page.width-40,
            ),
            margin=ft.margin.symmetric(horizontal=20)
        )

        # Assigned Team Members (Placeholder for now)
        assigned_section = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Assigned to", size=18, weight=ft.FontWeight.BOLD),
                    ft.Row(
                        [
                            ft.CircleAvatar(content=ft.Text("A")),
                            ft.CircleAvatar(content=ft.Text("B")),
                            ft.CircleAvatar(content=ft.Text("+"))
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    ),
                ],
                spacing=10
            ),
            padding=15,
            bgcolor="white",
            border_radius=10,
            width=page.width-40,
            margin=ft.margin.symmetric(horizontal=20)
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
                ],
                spacing=10
            ),
            padding=15,
            bgcolor="white",
            border_radius=10,
            width=page.width - 40,
            margin=ft.margin.symmetric(horizontal=20)
        )

        # Main content column
        content = ft.Column(
            [
                header,
                ngo_card,
                button_row,
                assigned_section,
                past_orders_section,
            ],
            spacing=20,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

        return content

    except Exception as e:
        print(f"Error in NGO desc: {e}")
        return ft.Text(f"Error loading page: {str(e)}", color="red")