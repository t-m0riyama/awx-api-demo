import flet as ft


class AppHeader(ft.UserControl):
    def __init__(self, page: ft.Page, view: ft.View, app_title):
        super().__init__()
        self.page = page
        self.view = view
        self.app_title = app_title
        self.toggle_dark_light_icon = ft.IconButton(
            icon='light_mode',
            selected_icon='dark_mode',
            tooltip='ライトモード/ダークモードの切り替え',
            on_click=self.toggle_icon,
        )
        self.appbar_items = [
            ft.PopupMenuItem(text='ログアウト', on_click=self.logout_clicked),
            # ft.PopupMenuItem(),
            # ft.PopupMenuItem(text='設定'),
        ]
        # appbarフィールドの設定
        self.view.appbar = ft.AppBar(
            leading=ft.Icon(ft.icons.HANDYMAN_OUTLINED),
            leading_width=100,
            title=ft.Text(value=self.app_title,
                          color=ft.colors.PRIMARY, size=28, text_align="center"),
            center_title=False,
            toolbar_height=46,
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                ft.Container(
                    content=ft.Row(
                        [
                            self.toggle_dark_light_icon,
                            ft.PopupMenuButton(
                                icon=ft.icons.ACCOUNT_CIRCLE,
                                items=self.appbar_items,
                                tooltip='アカウント設定',
                            ),
                        ],
                        alignment='spaceBetween',
                    ),
                    margin=ft.margin.only(left=50, right=25)
                )
            ],
        )

    def build(self):
        return self.view.appbar

    def toggle_icon(self, e):
        self.page.theme_mode = 'dark' if self.page.theme_mode == 'light' else 'light'
        self.page.update()
        self.toggle_dark_light_icon.selected = not self.toggle_dark_light_icon.selected
        self.page.update()

    def logout_clicked(self, e):
        e.page.go('/login')
