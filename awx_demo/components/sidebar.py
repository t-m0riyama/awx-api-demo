import flet as ft


class Sidebar(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.nav_rail_visible = True
        self.nav_rail_items = [
            ft.NavigationRailDestination(
                icon=ft.icons.LIST,
                selected_icon_content=ft.Icon(ft.icons.LIST_OUTLINED),
                label="申請の一覧"
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.CREATE_OUTLINED,
                selected_icon=ft.Icon(ft.icons.CREATE),
                label="申請の追加"
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.SETTINGS_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.SETTINGS),
                label_content=ft.Text("設定"),
            ),
        ]
        self.nav_rail = ft.NavigationRail(
            height=300,
            selected_index=None,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=400,
            # leading=ft.FloatingActionButton(icon=ft.icons.CREATE, text="ADD"),
            group_alignment=-0.9,
            destinations=self.nav_rail_items,
            on_change=lambda e: print(
                "Selected destination: ", e.control.selected_index),
        )
        self.toggle_nav_rail_button = ft.IconButton(
            icon=ft.icons.KEYBOARD_DOUBLE_ARROW_LEFT,
            icon_color=ft.colors.BLUE_GREY_400,
            selected=False,
            selected_icon=ft.icons.KEYBOARD_DOUBLE_ARROW_RIGHT,
            on_click=self.toggle_nav_rail,
            tooltip="サイドバーを非表示",
        )

    def build(self):
        self.view = ft.Container(
            content=ft.Row(
                [
                    self.nav_rail,
                    ft.Container(  # vertical divider
                        bgcolor=ft.colors.BLACK26,
                        border_radius=ft.border_radius.all(30),
                        height=220,
                        alignment=ft.alignment.center_right,
                        width=2
                    ),
                    self.toggle_nav_rail_button,
                ],
                expand=True,
                vertical_alignment=ft.CrossAxisAlignment.START,
                visible=self.nav_rail_visible,
            )
        )
        return self.view

    def toggle_nav_rail(self, e):
        self.nav_rail.visible = not self.nav_rail.visible
        self.toggle_nav_rail_button.selected = not self.toggle_nav_rail_button.selected
        self.toggle_nav_rail_button.tooltip = "サイドバーを表示" if self.toggle_nav_rail_button.selected else "Collapse Side Bar"
        self.view.update()
        self.page.update()
