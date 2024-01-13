import flet as ft

from awx_demo.components.app_header import AppHeader
from awx_demo.components.forms.select_target_form import SelectTargetForm


class SelectTargetView(ft.View):
    """Login View"""

    # const
    APP_TITLE = 'AWX API Demo'

    def __init__(self, session, page: ft.Page):
        formCreateRequest = SelectTargetForm(session)
        self.txtMesssage = ft.Text(size=24)

        controls = [
            formCreateRequest,
            ft.Divider(),
        ]
        super().__init__(
            route='/select_target',
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            controls=controls)
        AppHeader(page, self, self.APP_TITLE)
