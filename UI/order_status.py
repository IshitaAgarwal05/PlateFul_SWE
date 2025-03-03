import flet as ft

def main(page: ft.Page):
    # Set mobile-specific page configuration
    page.title = "Order Management"
    page.theme = ft.Theme(font_family="Roboto")  # Common mobile font
    page.padding = 0  # Remove default padding for mobile
    page.window_width = 375  # Adjusted to match iPhone width (closer to the image)
    page.window_height = 667  # Adjusted to match iPhone height (closer to the image)
    page.window_resizable = False  # Prevent resizing to PC-like dimensions

    # Colors from the image (exact matches)
    coral_bg = "#ff7f50"  # Coral background color
    white_bg = "#ffffff"  # White for order cards
    black_text = "#000000"  # Black for text (active tab)
    gray_text = "#666666"  # Gray for inactive tabs/secondary text/time/status
    yellow_bg = "#ffd700"  # Yellow for the "2 NEW ORDERS" button
    light_gray_border = "#e0e0e0"  # Light gray for order card borders

    # State to track the active tab
    active_tab = "ALL"  # Default to "ALL" for the initial page

    def update_tab_content(e):
        nonlocal active_tab
        if e.control.data == "ALL":
            active_tab = "ALL"
            page.go("/accepting")
        elif e.control.data == "PREPARING":
            active_tab = "PREPARING"
            page.go("/preparing")
        elif e.control.data == "READY":
            active_tab = "READY"
            page.go("/ready")
        update_ui()

    def update_ui():
        # Update tab colors using the tab_container_ref
        tab_row = tab_container_ref.current.content  # Access the Row from the container's content
        for control in tab_row.controls:
            if isinstance(control, ft.ElevatedButton):
                if control.data == active_tab:
                    control.bgcolor = black_text  # Black background for active tab
                    control.color = white_bg  # White text for active tab
                else:
                    control.bgcolor = None  # No background for inactive tabs
                    control.color = gray_text  # Gray text for inactive tabs
                control.update()
        page.update()

    def build_order_card(order_id, time, status, items, total, paid=False):
        return ft.Container(
            padding=ft.Padding(15, 10, 15, 10),  # More precise padding to match the image
            bgcolor=white_bg,
            border=ft.border.all(1, light_gray_border),  # Light gray border for cards
            border_radius=12,  # Slightly larger radius for a softer look
            margin=ft.Margin(15, 5, 15, 5),  # Adjusted margins for better spacing
            shadow=ft.BoxShadow(
                blur_radius=8,
                spread_radius=2,
                color=ft.Colors.with_opacity(0.12, ft.Colors.BLACK),  # Updated to use Colors.with_opacity
                offset=ft.Offset(0, 2)
            ),  # Subtle shadow for elevation
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(
                                f"ID: {order_id}",
                                size=16,  # Slightly larger for better readability
                                weight="bold",
                                color=black_text
                            ),
                            ft.Container(
                                content=ft.Text(
                                    time,
                                    size=14,  # Slightly larger for consistency
                                    color=gray_text,
                                    style=ft.TextStyle(italic=True)
                                ),
                                padding=ft.Padding(0, 0, 10, 0)  # Space before the dot
                            ),
                            ft.Icon(
                                ft.Icons.CIRCLE,
                                size=8,  # Smaller dot to match the image
                                color=gray_text
                            ),
                            ft.Container(
                                content=ft.Text(
                                    status,
                                    size=14,
                                    color=gray_text,
                                    style=ft.TextStyle(italic=True)
                                ),
                                padding=ft.Padding(10, 0, 0, 0)  # Space after the dot
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        spacing=5  # Tighter spacing for alignment
                    ),
                    ft.Text(
                        items,
                        size=16,  # Larger for readability
                        color=black_text,
                        height=1.5  # Use height to simulate line spacing (multiplier for line height)
                    ),
                    ft.Text(
                        f"Total Bill: ₹{total}",
                        size=18,  # Larger and bolder for emphasis
                        weight="bold",
                        color=black_text
                    ),
                    ft.Text(
                        "PAID" if paid else "",
                        size=14,
                        color=gray_text,
                        style=ft.TextStyle(italic=True)
                    )
                ],
                spacing=8  # Tighter spacing between rows in the column
            )
        )

    # Define content for each page
    accepting_orders = ft.Column(
        [
            build_order_card(
                "5635082",
                "4:18 PM",
                "Takeaway",
                "1 x Spring Veg Platter\n2 x Plant Protein Bowl",
                "50"
            ),
            build_order_card(
                "5635083",
                "4:20 PM",
                "Takeaway",
                "1 x Spring Veg Platter\n2 x Plant Protein Bowl",
                "50",
                paid=True
            )
        ],
        spacing=0
    )

    preparing_orders = ft.Column(
        [
            build_order_card(
                "5635082",
                "4:18 PM",
                "Takeaway",
                "1 x Spring Veg Platter\n2 x Plant Protein Bowl",
                "50"
            ),
            build_order_card(
                "5635083",
                "4:20 PM",
                "Takeaway",
                "1 x Spring Veg Platter\n2 x Plant Protein Bowl",
                "50"
            )
        ],
        spacing=0
    )

    ready_orders = ft.Column(
        [
            build_order_card(
                "5635080",
                "4:12 PM",
                "Takeaway",
                "1 x Spring Veg Platter\n2 x Plant Protein Bowl",
                "50",
                paid=True
            )
        ],
        spacing=0
    )

    # Create a reference for the tab container to access the Row
    tab_container_ref = ft.Ref[ft.Container]()

    def route_change(e):
        nonlocal active_tab
        if page.route == "/accepting":
            active_tab = "ALL"
        elif page.route == "/preparing":
            active_tab = "PREPARING"
        elif page.route == "/ready":
            active_tab = "READY"
        update_ui()
        # Update the page content dynamically
        page.clean()  # Clear current content
        page.add(build_page())  # Add new content based on the route

    # Set up route change handler
    page.on_route_change = route_change

    # Initial route (default to /accepting)
    page.go("/accepting")

    # Main content (dynamic based on route)
    def build_page():
        if page.route == "/accepting":
            return ft.Container(
                bgcolor=coral_bg,
                width=375,
                height=667,
                content=ft.Column(
                    [
                        # Header
                        ft.Container(
                            padding=ft.Padding(15, 10, 15, 10),
                            content=ft.Row(
                                [
                                    ft.IconButton(
                                        icon=ft.Icons.ARROW_BACK_IOS,
                                        icon_color=white_bg,
                                        icon_size=24,
                                        on_click=lambda e: page.go("/back")  # Placeholder navigation
                                    ),
                                    ft.Text(
                                        "Accepting Orders",
                                        size=24,
                                        weight="bold",
                                        color=white_bg
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT,
                                        icon_color=white_bg,
                                        icon_size=24,
                                        on_click=lambda e: page.go("/edit")  # Placeholder navigation
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                spacing=10
                            )
                        ),
                        # Tabs
                        ft.Container(
                            padding=ft.Padding(15, 10, 15, 10),
                            content=ft.Row(
                                ref=ft.Ref[ft.Row](),
                                controls=[
                                    ft.ElevatedButton(
                                        "ALL (2)",
                                        data="ALL",
                                        bgcolor=black_text if active_tab == "ALL" else None,
                                        color=white_bg if active_tab == "ALL" else gray_text,
                                        style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(radius=8),
                                            padding=ft.Padding(20, 10, 20, 10),
                                            elevation=0
                                        ),
                                        on_click=update_tab_content
                                    ),
                                    ft.ElevatedButton(
                                        "PREPARING (2)",
                                        data="PREPARING",
                                        bgcolor=black_text if active_tab == "PREPARING" else None,
                                        color=white_bg if active_tab == "PREPARING" else gray_text,
                                        style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(radius=8),
                                            padding=ft.Padding(20, 10, 20, 10),
                                            elevation=0
                                        ),
                                        on_click=update_tab_content
                                    ),
                                    ft.ElevatedButton(
                                        "READY (1)",
                                        data="READY",
                                        bgcolor=black_text if active_tab == "READY" else None,
                                        color=white_bg if active_tab == "READY" else gray_text,
                                        style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(radius=8),
                                            padding=ft.Padding(20, 10, 20, 10),
                                            elevation=0
                                        ),
                                        on_click=update_tab_content
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                spacing=5
                            ),
                            ref=tab_container_ref
                        ),
                        # Content
                        ft.Container(
                            content=accepting_orders,
                            expand=True
                        ),
                        # "2 NEW ORDERS" button
                        ft.Container(
                            alignment=ft.alignment.center,
                            margin=ft.Margin(15, 20, 15, 20),
                            content=ft.ElevatedButton(
                                "2 NEW ORDERS",
                                bgcolor=yellow_bg,
                                color=black_text,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=12),
                                    padding=ft.Padding(20, 15, 20, 15)
                                ),
                                icon=ft.Icon(ft.Icons.EXPAND_LESS, size=20),
                                icon_color=black_text
                            )
                        )
                    ],
                    spacing=0,
                    expand=True
                )
            )
        elif page.route == "/preparing":
            return ft.Container(
                bgcolor=coral_bg,
                width=375,
                height=667,
                content=ft.Column(
                    [
                        # Header
                        ft.Container(
                            padding=ft.Padding(15, 10, 15, 10),
                            content=ft.Row(
                                [
                                    ft.IconButton(
                                        icon=ft.Icons.ARROW_BACK_IOS,
                                        icon_color=white_bg,
                                        icon_size=24,
                                        on_click=lambda e: page.go("/back")  # Placeholder navigation
                                    ),
                                    ft.Text(
                                        "Preparing Orders",
                                        size=24,
                                        weight="bold",
                                        color=white_bg
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT,
                                        icon_color=white_bg,
                                        icon_size=24,
                                        on_click=lambda e: page.go("/edit")  # Placeholder navigation
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                spacing=10
                            )
                        ),
                        # Tabs
                        ft.Container(
                            padding=ft.Padding(15, 10, 15, 10),
                            content=ft.Row(
                                ref=ft.Ref[ft.Row](),
                                controls=[
                                    ft.ElevatedButton(
                                        "ALL (2)",
                                        data="ALL",
                                        bgcolor=black_text if active_tab == "ALL" else None,
                                        color=white_bg if active_tab == "ALL" else gray_text,
                                        style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(radius=8),
                                            padding=ft.Padding(20, 10, 20, 10),
                                            elevation=0
                                        ),
                                        on_click=update_tab_content
                                    ),
                                    ft.ElevatedButton(
                                        "PREPARING (2)",
                                        data="PREPARING",
                                        bgcolor=black_text if active_tab == "PREPARING" else None,
                                        color=white_bg if active_tab == "PREPARING" else gray_text,
                                        style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(radius=8),
                                            padding=ft.Padding(20, 10, 20, 10),
                                            elevation=0
                                        ),
                                        on_click=update_tab_content
                                    ),
                                    ft.ElevatedButton(
                                        "READY (1)",
                                        data="READY",
                                        bgcolor=black_text if active_tab == "READY" else None,
                                        color=white_bg if active_tab == "READY" else gray_text,
                                        style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(radius=8),
                                            padding=ft.Padding(20, 10, 20, 10),
                                            elevation=0
                                        ),
                                        on_click=update_tab_content
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                spacing=5
                            ),
                            ref=tab_container_ref
                        ),
                        # Content
                        ft.Container(
                            content=preparing_orders,
                            expand=True
                        ),
                        # "2 NEW ORDERS" button
                        ft.Container(
                            alignment=ft.alignment.center,
                            margin=ft.Margin(15, 20, 15, 20),
                            content=ft.ElevatedButton(
                                "2 NEW ORDERS",
                                bgcolor=yellow_bg,
                                color=black_text,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=12),
                                    padding=ft.Padding(20, 15, 20, 15)
                                ),
                                icon=ft.Icon(ft.Icons.EXPAND_LESS, size=20),
                                icon_color=black_text
                            )
                        )
                    ],
                    spacing=0,
                    expand=True
                )
            )
        elif page.route == "/ready":
            return ft.Container(
                bgcolor=coral_bg,
                width=375,
                height=667,
                content=ft.Column(
                    [
                        # Header
                        ft.Container(
                            padding=ft.Padding(15, 10, 15, 10),
                            content=ft.Row(
                                [
                                    ft.IconButton(
                                        icon=ft.Icons.ARROW_BACK_IOS,
                                        icon_color=white_bg,
                                        icon_size=24,
                                        on_click=lambda e: page.go("/back")  # Placeholder navigation
                                    ),
                                    ft.Text(
                                        "Ready Orders",
                                        size=24,
                                        weight="bold",
                                        color=white_bg
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT,
                                        icon_color=white_bg,
                                        icon_size=24,
                                        on_click=lambda e: page.go("/edit")  # Placeholder navigation
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                spacing=10
                            )
                        ),
                        # Tabs
                        ft.Container(
                            padding=ft.Padding(15, 10, 15, 10),
                            content=ft.Row(
                                ref=ft.Ref[ft.Row](),
                                controls=[
                                    ft.ElevatedButton(
                                        "ALL (2)",
                                        data="ALL",
                                        bgcolor=black_text if active_tab == "ALL" else None,
                                        color=white_bg if active_tab == "ALL" else gray_text,
                                        style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(radius=8),
                                            padding=ft.Padding(20, 10, 20, 10),
                                            elevation=0
                                        ),
                                        on_click=update_tab_content
                                    ),
                                    ft.ElevatedButton(
                                        "PREPARING (2)",
                                        data="PREPARING",
                                        bgcolor=black_text if active_tab == "PREPARING" else None,
                                        color=white_bg if active_tab == "PREPARING" else gray_text,
                                        style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(radius=8),
                                            padding=ft.Padding(20, 10, 20, 10),
                                            elevation=0
                                        ),
                                        on_click=update_tab_content
                                    ),
                                    ft.ElevatedButton(
                                        "READY (1)",
                                        data="READY",
                                        bgcolor=black_text if active_tab == "READY" else None,
                                        color=white_bg if active_tab == "READY" else gray_text,
                                        style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(radius=8),
                                            padding=ft.Padding(20, 10, 20, 10),
                                            elevation=0
                                        ),
                                        on_click=update_tab_content
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                spacing=5
                            ),
                            ref=tab_container_ref
                        ),
                        # Content
                        ft.Container(
                            content=ready_orders,
                            expand=True
                        ),
                        # "2 NEW ORDERS" button
                        ft.Container(
                            alignment=ft.alignment.center,
                            margin=ft.Margin(15, 20, 15, 20),
                            content=ft.ElevatedButton(
                                "2 NEW ORDERS",
                                bgcolor=yellow_bg,
                                color=black_text,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=12),
                                    padding=ft.Padding(20, 15, 20, 15)
                                ),
                                icon=ft.Icon(ft.Icons.EXPAND_LESS, size=20),
                                icon_color=black_text
                            )
                        )
                    ],
                    spacing=0,
                    expand=True
                )
            )
        else:
            # Default to /accepting route if no route is specified
            page.go("/accepting")
            return build_page()

    # Add the initial page content
    page.add(build_page())

ft.app(target=main)