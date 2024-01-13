import flet as ft

from awx_demo.components.app_header import AppHeader
from awx_demo.components.forms.create_request_form import CreateRequestForm


class CreateRequestView(ft.View):
    """申請の新規作成 View"""

    # const
    APP_TITLE = 'AWX API Demo'

    def __init__(self, session, page: ft.Page):
        formCreateRequest = CreateRequestForm(session)
        self.txtMesssage = ft.Text(size=24)

        controls = [
            formCreateRequest,
            ft.Divider(),
        ]
        super().__init__(
            route="/create_request",
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            controls=controls)
        AppHeader(page, self, self.APP_TITLE)
