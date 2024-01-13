import os
import flet as ft

from awx_demo.components.forms.login_form import LoginForm


class LoginView(ft.View):
    """Login View"""

    # const
    DEFAULT_awx_url = 'https://gzbox01.moriyama.internal:8043'

    def __init__(self, session, page: ft.Page):
        default_awx_url = os.getenv('awx_url', self.DEFAULT_awx_url)
        formLogin = LoginForm(session=session, page=page,
                              default_awx_url=default_awx_url)
        controls = [
            formLogin,
        ]
        super().__init__(
            route='/login',
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            controls=controls
        )
