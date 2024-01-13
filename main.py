import os
import logging
import flet as ft

from awx_demo.components.views.create_request_view import CreateRequestView
from awx_demo.components.views.select_target_view import SelectTargetView
from awx_demo.components.views.set_vm_cpu_memory_view import SetVmCpuMemoryView
from awx_demo.components.views.set_vm_cpu_memory_confirm_view import SetVmCpuMemoryConfirmView
from awx_demo.components.views.job_progress_view import JobProgressView
from awx_demo.components.views.login_view import LoginView

# const
DEFAULT_FLET_PATH = 'app'
DEFAULT_FLET_PORT = 8888


def main(page: ft.Page):

    def route_change(e):
        nonlocal pop_flag

        if pop_flag:
            pop_flag = False
        else:
            if page.route == '/login':
                page.views.clear()
                page.views.append(
                    LoginView(session=page.session, page=page)
                )
            elif page.route == '/create_request':
                page.views.append(
                    CreateRequestView(session=page.session, page=page)
                )
            elif page.route == '/select_target':
                page.views.append(
                    SelectTargetView(session=page.session, page=page)
                )
            elif page.route == '/set_vm_cpu_memory':
                page.views.append(
                    SetVmCpuMemoryView(session=page.session, page=page)
                )
            elif page.route == '/set_vm_cpu_memory_confirm':
                page.views.append(
                    SetVmCpuMemoryConfirmView(session=page.session, page=page)
                )
            elif page.route == '/job_progress':
                page.views.append(
                    JobProgressView(session=page.session, page=page)
                )

    def view_pop(e):
        nonlocal pop_flag

        pop_flag = True
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    pop_flag = False

    # Page レイアウト
    page.title = 'AWX API Demo'
    page.padding = 10
    page.window_height = 600
    page.window_width = 800

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.theme_mode = 'light'
    page.views.clear()
    page.go('/login')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    # for develop
    flet_path = os.getenv("FLET_PATH", DEFAULT_FLET_PATH)
    flet_port = int(os.getenv('FLET_PORT', DEFAULT_FLET_PORT))
    ft.app(name=flet_path, target=main, port=flet_port, view=None)

    # for packaging
    # ft.app(target=main)
