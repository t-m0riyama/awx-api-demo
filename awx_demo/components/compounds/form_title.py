import flet as ft


class FormTitle(ft.UserControl):

    def __init__(self, title, sub_title, width):
        self.title = title
        self.sub_title = sub_title
        self.title_width = width
        super().__init__()

    def build(self):
        return ft.Column(
            [
                ft.Container(
                    ft.Text(
                        value=self.title,
                        # style=ft.TextThemeStyle.DISPLAY_MEDIUM,
                        size=30,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.ON_SECONDARY,
                        width=self.title_width,
                        text_align=ft.TextAlign.CENTER
                    ),
                    bgcolor=ft.colors.SECONDARY,
                ),

                ft.Text(
                    value=self.sub_title,
                    # style=ft.TextThemeStyle.DISPLAY_SMALL,
                    size=24,
                    weight=ft.FontWeight.NORMAL,
                    width=self.title_width,
                    text_align=ft.TextAlign.CENTER
                ),
            ]
        )
