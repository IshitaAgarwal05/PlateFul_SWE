import flet as ft

def onboarding_page_1(page):
    return ft.View(
        "/page1",
        controls=[
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.icons.APP_SETTINGS_ALT_OUTLINED, size=100, color="deeporange"),
                    ft.Text("Welcome to Plateful", size=30, weight="bold"),
                    ft.Text("Your personalized food companion.", size=18, color="grey"),
                    ft.ProgressRing(color="deeporange", width=30, height=30),
                    ft.ElevatedButton("Next", on_click=lambda e: page.go("/page2"))
                ], alignment="center", horizontal_alignment="center", spacing=20),
                alignment=ft.alignment.center,
                expand=True
            )
        ]
    )

def onboarding_page_2(page):
    return ft.View(
        "/page2",
        controls=[
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.icons.SEARCH, size=100, color="green"),
                    ft.Text("Explore Restaurants", size=30, weight="bold"),
                    ft.Text("Find the best places to eat around you.", size=18, color="grey"),
                    ft.ElevatedButton("Next", on_click=lambda e: page.go("/page3"))
                ], alignment="center", horizontal_alignment="center", spacing=20),
                alignment=ft.alignment.center,
                expand=True
            )
        ]
    )

def onboarding_page_3(page):
    return ft.View(
        "/page3",
        controls=[
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.icons.SHOPPING_CART, size=100, color="blue"),
                    ft.Text("Order with Ease", size=30, weight="bold"),
                    ft.Text("Quick and seamless food ordering.", size=18, color="grey"),
                    ft.ElevatedButton("Next", on_click=lambda e: page.go("/page4"))
                ], alignment="center", horizontal_alignment="center", spacing=20),
                alignment=ft.alignment.center,
                expand=True
            )
        ]
    )

def onboarding_page_4(page):
    return ft.View(
        "/page4",
        controls=[
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.icons.LOCAL_SHIPPING, size=100, color="orange"),
                    ft.Text("Track Your Orders", size=30, weight="bold"),
                    ft.Text("Stay updated in real-time.", size=18, color="grey"),
                    ft.ElevatedButton("Next", on_click=lambda e: page.go("/page5"))
                ], alignment="center", horizontal_alignment="center", spacing=20),
                alignment=ft.alignment.center,
                expand=True
            )
        ]
    )

def onboarding_page_5(page):
    return ft.View(
        "/page5",
        controls=[
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.icons.FAVORITE_BORDER, size=100, color="red"),
                    ft.Text("Save Your Favorites", size=30, weight="bold"),
                    ft.Text("Quickly reorder your favorite meals.", size=18, color="grey"),
                    ft.ElevatedButton("Next", on_click=lambda e: page.go("/page6"))
                ], alignment="center", horizontal_alignment="center", spacing=20),
                alignment=ft.alignment.center,
                expand=True
            )
        ]
    )

def onboarding_page_6(page, navigate_to):
    return ft.View(
        "/page6",
        controls=[
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.icons.CHECK_CIRCLE_OUTLINE, size=100, color="teal"),
                    ft.Text("You're All Set!", size=30, weight="bold"),
                    ft.Text("Let’s get started.", size=18, color="grey"),
                    ft.ElevatedButton("Finish", on_click=lambda e: navigate_to(page, "login", email=None))
                ], alignment="center", horizontal_alignment="center", spacing=20),
                alignment=ft.alignment.center,
                expand=True
            )
        ]
    )

def onboarding(page: ft.Page, navigate_to):
    page.title = "Onboarding Screens"
    page.bgcolor = ft.colors.WHITE

    def route_change(e):
        page.views.clear()
        route = page.route

        if route == "/":
            page.go("/page1")
        elif route == "/page1":
            page.views.append(onboarding_page_1(page))
        elif route == "/page2":
            page.views.append(onboarding_page_2(page))
        elif route == "/page3":
            page.views.append(onboarding_page_3(page))
        elif route == "/page4":
            page.views.append(onboarding_page_4(page))
        elif route == "/page5":
            page.views.append(onboarding_page_5(page))
        elif route == "/page6":
            page.views.append(onboarding_page_6(page, navigate_to))

        page.update()

    page.on_route_change = route_change
    page.go(page.route)