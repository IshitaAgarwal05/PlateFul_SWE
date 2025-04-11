import flet as ft

def onboarding(page: ft.Page, navigate_to):
    def onboarding_page(icon, title, subtitle, btn_text, next_view_func, show_loader=False, is_first=False, image_src=None, show_skip=False, page_index=0, total_pages=6):
        if is_first:
            return ft.Container(
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_left,
                    end=ft.alignment.bottom_right,
                    colors=["#FF0000", "#FFFF00"]
                ),
                content=ft.Column([
                    ft.Image(
                        src="assets/images/elements/general/1_white.png",
                        width=200,
                        height=200,
                        fit=ft.ImageFit.CONTAIN
                    ),
                    ft.Text("Version 1.0", size=16, color="white"),
                    ft.Text("PlateFul hai toh,\nPet full hai!", size=22, weight="bold", color="white", text_align="center"),
                    ft.ProgressRing(width=40, height=40, color="deeporange"),
                    ft.ElevatedButton("Next", on_click=next_view_func)
                ],
                    alignment="center",
                    horizontal_alignment="center",
                    spacing=25
                ),
                alignment=ft.alignment.center,
                expand=True,
                padding=20,
                border_radius=0
            )

        # Page indicator (dots)
        indicators = []
        for i in range(total_pages):
            indicators.append(
                ft.Container(
                    width=12,
                    height=12,
                    margin=ft.margin.symmetric(horizontal=4),
                    border_radius=6,
                    bgcolor="#FF7043" if i == page_index else "#FFE0B2"
                )
            )

        content = []

        if image_src:
            content.append(ft.Image(
                src=image_src,
                width=180,
                height=180,
                fit=ft.ImageFit.CONTAIN
            ))
        elif icon:
            content.append(ft.Icon(icon, size=100, color="deeporange"))

        content.extend([
            ft.Text(title, size=20, weight="bold", color="#FF7043"),
            ft.Text(subtitle, size=16, color="grey", text_align="center"),
            ft.Row(indicators, alignment="center", spacing=0),
            ft.Container(
                content=ft.ElevatedButton(
                    btn_text,
                    on_click=next_view_func,
                    bgcolor="#FF7043",
                    color="white",
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=30))
                ),
                margin=10
            )
        ])

        if show_skip:
            content.append(
                ft.TextButton("Skip", on_click=lambda e: navigate_to(page, "login", email=None))
            )

        return ft.Container(
            content=ft.Column(content, alignment="center", horizontal_alignment="center", spacing=15),
            alignment=ft.alignment.center,
            expand=True,
            padding=20
        )

    def show_page(index):
        page.controls.clear()
        screens = [
            onboarding_page(
                None, "", "", "Next",
                lambda e: show_page(1),
                show_loader=True,
                is_first=True,
                page_index=0
            ),
            onboarding_page(
                None,
                "Widely Assorted Foods",
                "Different varieties of food available.",
                "Next",
                lambda e: show_page(2),
                image_src="assets/images/elements/general/image4.png",
                show_skip=True,
                page_index=1
            ),
            onboarding_page(
                None,
                "Cheapest Of All",
                "Get food at more than 50% discount. \n Weekly deals and discounts",
                "Next",
                lambda e: show_page(3),
                image_src="assets/images/elements/general/image5.png",
                show_skip=True,
                page_index=2
            ),
            onboarding_page(
                ft.icons.SHOPPING_CART,
                "Order with Ease",
                "Quick and seamless food ordering.",
                "Next",
                lambda e: show_page(4),
                show_skip=True,
                page_index=3
            ),
            onboarding_page(
                None,
                "High Quality",
                "Quality food assured.",
                "Next",
                lambda e: show_page(5),
                image_src="assets/images/elements/general/image6.png",
                show_skip=True,
                page_index=4
            ),
            onboarding_page(
                ft.icons.FAVORITE_BORDER,
                "Save Your Favorites",
                "Quickly reorder your favorite meals.",
                "Next",
                lambda e: show_page(6),
                show_skip=True,
                page_index=5
            ),
            onboarding_page(
                ft.icons.CHECK_CIRCLE_OUTLINE,
                "You're All Set!",
                "Let’s get started.",
                "Finish",
                lambda e: navigate_to(page, "login", email=None),
                page_index=6
            )
        ]

        page.controls.append(screens[index])
        page.update()

    show_page(0)