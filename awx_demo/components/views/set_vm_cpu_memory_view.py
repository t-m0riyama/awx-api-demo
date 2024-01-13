import flet as ft

from awx_demo.components.app_header import AppHeader
from awx_demo.components.forms.set_vm_cpu_memory_form import SetVmCpuMemoryForm


class SetVmCpuMemoryView(ft.View):
    """Login View"""

    # const
    APP_TITLE = 'AWX API Demo'

    def __init__(self, session, page: ft.Page):
        formCreateRequest = SetVmCpuMemoryForm(session)
        self.txtMesssage = ft.Text(size=24)

        controls = [
            formCreateRequest,
            ft.Divider(),
        ]
        super().__init__(
            route='/set_vm_cpu_memory',
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            controls=controls)
        AppHeader(page, self, self.APP_TITLE)
