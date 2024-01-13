import flet as ft

from awx_demo.components.app_header import AppHeader
from awx_demo.components.forms.job_progress_form import JobProgressForm


class JobProgressView(ft.View):
    """JobProgress View"""

    # const
    APP_TITLE = 'AWX API Demo'

    def __init__(self, session, page: ft.Page):
        formCreateRequest = JobProgressForm(session)
        self.txtMesssage = ft.Text(size=24)

        controls = [
            formCreateRequest,
            ft.Divider(),
        ]
        super().__init__(
            route='/job_progress',
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            controls=controls)
        AppHeader(page, self, self.APP_TITLE)
