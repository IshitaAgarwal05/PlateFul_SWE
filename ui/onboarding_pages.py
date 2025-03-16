import flet as ft

def onboard_page(page: ft.Page, navigate_to):
    page.title = "Plateful Onboarding"
    page.bgcolor = ft.colors.WHITE

    def go_next(e):
        if e.control.data == 1:
            page.clean()
            page.add(step_2)
        elif e.control.data == 2:
            page.clean()
            page.add(step_3)
        elif e.control.data == 3:
            page.clean()
            page.add(step_4)
        else:
            page.clean()
            page.add(login_page)
        page.update()

    splash_screen = ft.Container(
        content=ft.Column([
            ft.Image(src="assets/images/1_white.png", width=200, height=200),
            ft.Text("Plateful hai toh, Pet full hai!", size=24, weight=ft.FontWeight.BOLD),
            ft.ProgressBar(width=300)
        ], alignment=ft.MainAxisAlignment.CENTER),
        alignment=ft.alignment.center,
        bgcolor=ft.LinearGradient(colors=[ft.colors.RED, ft.colors.YELLOW],
                                  begin=ft.alignment.top_left, end=ft.alignment.bottom_right)
    )

    step_1 = ft.Column([
        ft.Image(src="assets/images/image_1.png", width=300),
        ft.Text("Widely Assorted Foods", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.RED),
        ft.Text("Different varieties of food available."),
        ft.ElevatedButton("Next", on_click=go_next, data=1)
    ], alignment=ft.MainAxisAlignment.CENTER)

    step_2 = ft.Column([
        ft.Image(src="assets/images/image_2.png", width=300),
        ft.Text("Cheapest Of All", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.RED),
        ft.Text("Get food at more than 50% discount."),
        ft.ElevatedButton("Next", on_click=go_next, data=2)
    ], alignment=ft.MainAxisAlignment.CENTER)

    step_3 = ft.Column([
        ft.Icon(ft.icons.VERIFIED, size=100),
        ft.Text("High Quality", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.RED),
        ft.Text("High Quality food assured."),
        ft.ElevatedButton("Next", on_click=go_next, data=3)
    ], alignment=ft.MainAxisAlignment.CENTER)

    step_4 = ft.Column([
        ft.Image(src="assets/images/special_offers.png", width=300),
        ft.Text("Special Offers", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.RED),
        ft.Text("Weekly deals and discounts."),
        ft.ElevatedButton("Start enjoying", on_click=go_next, data=4),
        ft.TextButton("Login / Registration")
    ], alignment=ft.MainAxisAlignment.CENTER)

    login_page = ft.Column([
        ft.Text("Welcome to Plateful!", size=24, weight=ft.FontWeight.BOLD),
        ft.Text("Please log in or register to start ordering delicious food!"),
        ft.ElevatedButton("Login / Register")
    ], alignment=ft.MainAxisAlignment.CENTER)

    # Return the splash screen as the initial content
    return splash_screen
