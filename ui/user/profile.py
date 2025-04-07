import flet as ft

def profile(page: ft.Page, navigate_to, email):
    # Set strict mobile-specific page configuration
    page.title = "Profile"
    page.theme = ft.Theme(font_family="Roboto")  # Common mobile font
    page.padding = 0  # Remove default padding for mobile
    page.window_width = 360  # Fixed mobile width (small phone)
    page.window_height = 640  # Fixed mobile height
    page.window_resizable = False  # Prevent resizing to PC-like dimensions

    # Sample profile data (you can replace these with dynamic data)
    profile_name = "Amit Sinhal"
    profile_phone = "+91 94254 76655"
    profile_email = "amitsinhal@jklu.edu.in"

    # Dark mode state (set to False by default for light mode)
    dark_mode = False  # Default to light mode
    light_bg = "#ffffff"  # White background for light mode
    dark_bg = "#333333"  # Dark gray background for dark mode
    light_text = "black"  # Text color for light mode
    dark_text = "white"  # Text color for dark mode

    def update_theme():
        # Update all containers and their nested content
        for control in page.controls:
            if isinstance(control, ft.Container):
                control.bgcolor = dark_bg if dark_mode else light_bg
                # Explicitly update nested content
                if control.content:
                    update_container_theme(control.content)
        page.update()

    def update_container_theme(content):
        # Recursively update all controls within containers
        if isinstance(content, (ft.Stack, ft.ListView, ft.Column, ft.Row)):
            for child in content.controls:
                if isinstance(child, ft.Container):
                    child.bgcolor = dark_bg if dark_mode else light_bg
                    if child.content:
                        update_container_theme(child.content)
                elif isinstance(child, ft.Text):
                    child.color = dark_text if dark_mode else light_text
                    child.update()
                elif isinstance(child, ft.IconButton):
                    child.icon_color = dark_text if dark_mode else light_text
                    child.update()
                elif isinstance(child, ft.ListTile):
                    if child.title:
                        child.title.color = dark_text if dark_mode else light_text
                        child.title.update()
                    if child.leading:
                        child.leading.color = dark_text if dark_mode else light_text
                        child.leading.update()
                    if child.trailing:
                        child.trailing.color = dark_text if dark_mode else light_text
                        child.trailing.update()
                    child.update()
                elif isinstance(child, ft.ElevatedButton):
                    # Buttons retain their custom colors, no change needed
                    child.update()
                elif isinstance(child, ft.Dropdown):
                    child.bgcolor = dark_bg if dark_mode else light_bg
                    child.border_color = dark_text if dark_mode else light_text
                    for option in child.options:
                        option.style = ft.TextStyle(color=dark_text if dark_mode else light_text)
                    child.update()
                elif isinstance(child, ft.Switch):
                    child.thumb_color = dark_text if dark_mode else light_text
                    child.track_color = dark_bg if dark_mode else light_bg
                    child.update()
        elif isinstance(content, ft.Text):
            content.color = dark_text if dark_mode else light_text
            content.update()

    def on_dark_mode_change(e):
        nonlocal dark_mode
        dark_mode = e.control.value
        update_theme()

    # Define the profile page content first, then apply theme
    main_container = ft.Container(
        content=ft.Stack(
            [
                # Gradient background on the left edge (simulating card effect)
                ft.Container(
                    width=20,
                    height=640,
                    gradient=ft.LinearGradient(
                        begin=ft.Alignment(-1.0, -1.0),  # Top-left
                        end=ft.Alignment(1.0, 1.0),      # Bottom-right
                        colors=[dark_bg if dark_mode else "#f5f5f5", dark_bg if dark_mode else "#ffffff"]  # Dynamic gradient
                    ),
                    left=0
                ),
                # Main content with dynamic background and scrollable list
                ft.Container(
                    margin=ft.Margin(left=20, top=0, right=0, bottom=0),
                    bgcolor=dark_bg if dark_mode else light_bg,
                    width=340,
                    height=640,
                    content=ft.ListView(
                        controls=[
                            # Header with back arrow and title
                            ft.Container(
                                content=ft.Row(
                                    [
                                        ft.IconButton(
                                            icon=ft.Icons.ARROW_BACK,
                                            icon_color=dark_text if dark_mode else light_text,
                                            style=ft.ButtonStyle(
                                                shape=ft.RoundedRectangleBorder(radius=8),
                                                padding=ft.Padding(8, 8, 8, 8)
                                            ),
                                            icon_size=20
                                        ),
                                        ft.Text(
                                            "Profile",
                                            size=20,
                                            color=dark_text if dark_mode else light_text,
                                            weight="bold"
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.MORE_VERT,
                                            icon_color=dark_text if dark_mode else light_text,
                                            style=ft.ButtonStyle(
                                                shape=ft.RoundedRectangleBorder(radius=8),
                                                padding=ft.Padding(8, 8, 8, 8)
                                            ),
                                            icon_size=20
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    spacing=10
                                ),
                                padding=10,
                                bgcolor=dark_bg if dark_mode else light_bg,
                                width=340
                            ),
                            # Profile section
                            ft.Container(
                                padding=20,
                                content=ft.Column(
                                    [
                                        ft.Row(
                                            [
                                                ft.CircleAvatar(
                                                    content=ft.Image(
                                                        src="https://via.placeholder.com/50",
                                                        width=50,
                                                        height=50,
                                                        fit=ft.ImageFit.COVER
                                                    ),
                                                    radius=25
                                                ),
                                                ft.Column(
                                                    [
                                                        ft.Text(
                                                            profile_name,
                                                            size=16,
                                                            color=dark_text if dark_mode else light_text,
                                                            weight="bold"
                                                        ),
                                                        ft.Text(
                                                            profile_phone,
                                                            size=14,
                                                            color="#999999" if dark_mode else "#666666"
                                                        ),
                                                        ft.Text(
                                                            profile_email,
                                                            size=14,
                                                            color="#999999" if dark_mode else "#666666"
                                                        )
                                                    ],
                                                    spacing=5,
                                                    alignment=ft.MainAxisAlignment.CENTER
                                                ),
                                                ft.IconButton(
                                                    icon=ft.Icons.EDIT,
                                                    icon_color="#ff7f50",
                                                    style=ft.ButtonStyle(
                                                        shape=ft.RoundedRectangleBorder(radius=8),
                                                        padding=ft.Padding(8, 8, 8, 8)
                                                    ),
                                                    icon_size=20
                                                )
                                            ],
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            spacing=15
                                        ),
                                        ft.ElevatedButton(
                                            "Logout",
                                            bgcolor="#ff7f50",
                                            color="white",
                                            style=ft.ButtonStyle(
                                                shape=ft.RoundedRectangleBorder(radius=8),
                                                padding=ft.Padding(12, 8, 12, 8)
                                            ),
                                            width=200
                                        )
                                    ],
                                    spacing=20,
                                    alignment=ft.MainAxisAlignment.CENTER
                                ),
                                bgcolor=dark_bg if dark_mode else light_bg,
                                width=340
                            ),
                            # Menu items
                            ft.Container(
                                padding=10,
                                content=ft.Column(
                                    [
                                        ft.ListTile(
                                            leading=ft.Icon(ft.Icons.LOCATION_ON, size=20, color=dark_text if dark_mode else light_text),
                                            title=ft.Text("My Locations", size=14, color=dark_text if dark_mode else light_text),
                                            trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT, size=20, color=dark_text if dark_mode else light_text),
                                            on_click=lambda e: page.go("/locations")
                                        ),
                                        ft.ListTile(
                                            leading=ft.Icon(ft.Icons.STAR, size=20, color=dark_text if dark_mode else light_text),
                                            title=ft.Text("My Promotions", size=14, color=dark_text if dark_mode else light_text),
                                            trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT, size=20, color=dark_text if dark_mode else light_text),
                                            on_click=lambda e: page.go("/promotions")
                                        ),
                                        ft.ListTile(
                                            leading=ft.Icon(ft.Icons.PAYMENT, size=20, color=dark_text if dark_mode else light_text),
                                            title=ft.Text("Payment Methods", size=14, color=dark_text if dark_mode else light_text),
                                            trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT, size=20, color=dark_text if dark_mode else light_text),
                                            on_click=lambda e: page.go("/payment_methods")
                                        ),
                                        ft.ListTile(
                                            leading=ft.Icon(ft.Icons.MESSAGE, size=20, color=dark_text if dark_mode else light_text),
                                            title=ft.Text("Messages", size=14, color=dark_text if dark_mode else light_text),
                                            trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT, size=20, color=dark_text if dark_mode else light_text),
                                            on_click=lambda e: page.go("/messages")
                                        ),
                                        ft.ListTile(
                                            leading=ft.Icon(ft.Icons.PERSON_ADD, size=20, color=dark_text if dark_mode else light_text),
                                            title=ft.Text("Invite Friends", size=14, color=dark_text if dark_mode else light_text),
                                            trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT, size=20, color=dark_text if dark_mode else light_text),
                                            on_click=lambda e: page.go("/invite_friends")
                                        ),
                                        ft.ListTile(
                                            leading=ft.Icon(ft.Icons.SECURITY, size=20, color=dark_text if dark_mode else light_text),
                                            title=ft.Text("Security", size=14, color=dark_text if dark_mode else light_text),
                                            trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT, size=20, color=dark_text if dark_mode else light_text),
                                            on_click=lambda e: page.go("/security")
                                        ),
                                        ft.ListTile(
                                            leading=ft.Icon(ft.Icons.HELP, size=20, color=dark_text if dark_mode else light_text),
                                            title=ft.Text("Help Center", size=14, color=dark_text if dark_mode else light_text),
                                            trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT, size=20, color=dark_text if dark_mode else light_text),
                                            on_click=lambda e: page.go("/help_center")
                                        )
                                    ],
                                    spacing=5
                                ),
                                bgcolor=dark_bg if dark_mode else light_bg,
                                width=340
                            ),
                            # Settings options
                            ft.Container(
                                padding=10,
                                content=ft.Column(
                                    [
                                        ft.ListTile(
                                            title=ft.Text("Language", size=14, color=dark_text if dark_mode else light_text),
                                            trailing=ft.Dropdown(
                                                value="English",
                                                options=[
                                                    ft.dropdown.Option("English", style=ft.TextStyle(color=dark_text if dark_mode else light_text)),
                                                    ft.dropdown.Option("Spanish", style=ft.TextStyle(color=dark_text if dark_mode else light_text)),
                                                    ft.dropdown.Option("French", style=ft.TextStyle(color=dark_text if dark_mode else light_text))
                                                ],
                                                width=100,
                                                bgcolor=dark_bg if dark_mode else light_bg,
                                                border_color=dark_text if dark_mode else light_text
                                            )
                                        ),
                                        ft.ListTile(
                                            title=ft.Text("Push Notification", size=14, color=dark_text if dark_mode else light_text),
                                            trailing=ft.Switch(value=True, thumb_color=dark_text if dark_mode else light_text, track_color=dark_bg if dark_mode else light_bg)
                                        ),
                                        ft.ListTile(
                                            title=ft.Text("Dark Mode", size=14, color=dark_text if dark_mode else light_text),
                                            trailing=ft.Switch(value=dark_mode, thumb_color=dark_text if dark_mode else light_text, track_color=dark_bg if dark_mode else light_bg, on_change=on_dark_mode_change)
                                        ),
                                        ft.ListTile(
                                            title=ft.Text("Sound", size=14, color=dark_text if dark_mode else light_text),
                                            trailing=ft.Switch(value=True, thumb_color=dark_text if dark_mode else light_text, track_color=dark_bg if dark_mode else light_bg)
                                        ),
                                        ft.ListTile(
                                            title=ft.Text("Automatically Updated", size=14, color=dark_text if dark_mode else light_text),
                                            trailing=ft.Switch(value=False, thumb_color=dark_text if dark_mode else light_text, track_color=dark_bg if dark_mode else light_bg)
                                        )
                                    ],
                                    spacing=5
                                ),
                                bgcolor=dark_bg if dark_mode else light_bg,
                                width=340
                            ),
                            # Additional menu items
                            ft.Container(
                                padding=10,
                                content=ft.Column(
                                    [
                                        ft.ListTile(
                                            title=ft.Text("Terms of Service", size=14, color=dark_text if dark_mode else light_text),
                                            trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT, size=20, color=dark_text if dark_mode else light_text),
                                            on_click=lambda e: page.go("/terms")
                                        ),
                                        ft.ListTile(
                                            title=ft.Text("Privacy Policy", size=14, color=dark_text if dark_mode else light_text),
                                            trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT, size=20, color=dark_text if dark_mode else light_text),
                                            on_click=lambda e: page.go("/privacy")
                                        ),
                                        ft.ListTile(
                                            title=ft.Text("About App", size=14, color=dark_text if dark_mode else light_text),
                                            trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT, size=20, color=dark_text if dark_mode else light_text),
                                            on_click=lambda e: page.go("/about")
                                        )
                                    ],
                                    spacing=5
                                ),
                                bgcolor=dark_bg if dark_mode else light_bg,
                                width=340
                            ),
                            # Bottom navigation bar
                            ft.Container(
                                content=ft.Row(
                                    [
                                        ft.IconButton(
                                            icon=ft.Icons.HOME,
                                            icon_color=dark_text if dark_mode else light_text,
                                            icon_size=24,
                                            on_click=lambda e: page.go("/home")
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.LIST,
                                            icon_color=dark_text if dark_mode else light_text,
                                            icon_size=24,
                                            on_click=lambda e: page.go("/list")
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.FAVORITE,
                                            icon_color=dark_text if dark_mode else light_text,
                                            icon_size=24,
                                            on_click=lambda e: page.go("/favorites")
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.NOTIFICATIONS,
                                            icon_color=dark_text if dark_mode else light_text,
                                            icon_size=24,
                                            on_click=lambda e: page.go("/notifications")
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.PERSON,
                                            icon_color="#ff7f50",
                                            icon_size=24,
                                            on_click=lambda e: page.go("/profile")
                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                    spacing=10
                                ),
                                padding=10,
                                bgcolor=dark_bg if dark_mode else light_bg,
                                width=340
                            )
                        ]
                    )
                )
            ]
        ),
        width=360,
        height=640
    )

    # Add the main container to the page
    page.add(main_container)

    # Apply initial theme after adding controls
    update_theme()

    # Debug print to confirm window size
    print(f"Window size: {page.window_width}x{page.window_height}, Resizable: {page.window_resizable}")


