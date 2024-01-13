import flet as ft

from awx_demo.components.compounds.form_title import FormTitle
from awx_demo.components.compounds.form_description import FormDescription
from awx_demo.awx_api.awx_api_helper import AWXApiHelper


class SetVmCpuMemoryConfirmForm(ft.UserControl):

    # const
    CONTENT_HEIGHT = 500
    CONTENT_WIDTH = 700
    BODY_HEIGHT = 250
    JOB_TEMPLATE_NAME = 'vm-config-utils_set_vm_cpu'
    VARS_TEMPLATE_NAME = 'aap_demo_extra_vars'

    def __init__(self, session):
        self.session = session
        super().__init__()

    def build(self):
        formTitle = FormTitle('CPU/メモリ割り当て変更', '変更内容の確認', self.CONTENT_WIDTH)
        formDescription = FormDescription('以下の内容で、変更を適用します。')
        self.checkShutdownBeforeChange = ft.Checkbox(
            label='設定変更前に、仮想マシンを停止する', value=True)
        self.checkStartupAfterChange = ft.Checkbox(
            label='設定変更後に、仮想マシンを起動する', value=True)
        self.lvConfirmParams = ft.ListView(
            # expand=1,
            spacing=10,
            padding=10,
            auto_scroll=True)
        self.lvConfirmParams.controls.append(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(
                                value='クラスタ',
                                style=ft.TextThemeStyle.BODY_LARGE,
                                color=ft.colors.PRIMARY),
                            ft.Text(value=self.session.get('vsphere_cluster'),
                                    style=ft.TextThemeStyle.BODY_LARGE,
                                    color=ft.colors.SECONDARY),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    ft.Row(
                        [
                            ft.Text(
                                value='仮想マシン',
                                style=ft.TextThemeStyle.BODY_LARGE,
                                color=ft.colors.PRIMARY),
                            ft.Text(value=self.session.get('target_vms'),
                                    style=ft.TextThemeStyle.BODY_LARGE,
                                    color=ft.colors.SECONDARY),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    ft.Row(
                        [
                            ft.Text(
                                value='CPUコア数',
                                style=ft.TextThemeStyle.BODY_LARGE,
                                color=ft.colors.PRIMARY),
                            ft.Text(value=self.session.get('vcpus'),
                                    style=ft.TextThemeStyle.BODY_LARGE,
                                    color=ft.colors.SECONDARY),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    ft.Row(
                        [
                            ft.Text(
                                value='メモリ容量(GB)',
                                style=ft.TextThemeStyle.BODY_LARGE,
                                color=ft.colors.PRIMARY),
                            ft.Text(value=self.session.get('memory_gb'),
                                    style=ft.TextThemeStyle.BODY_LARGE,
                                    color=ft.colors.SECONDARY),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    )
                ]
            )
        )

        self.btnNext = ft.FilledButton(
            '適用', on_click=self.apply_clicked)
        self.btnPrev = ft.ElevatedButton(
            '戻る', on_click=self.prev_clicked)
        self.btnCancel = ft.ElevatedButton(
            'キャンセル', on_click=self.cancel_clicked)

        # Content
        header = ft.Container(
            formTitle,
            margin=ft.margin.only(bottom=20),
        )
        body = ft.Column(
            [
                formDescription,
                self.checkShutdownBeforeChange,
                self.checkStartupAfterChange,
                self.lvConfirmParams,
            ],
            height=self.BODY_HEIGHT,
        )
        footer = ft.Row(
            [
                self.btnCancel,
                self.btnPrev,
                self.btnNext,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        return ft.Card(
            ft.Container(
                ft.Column(
                    [
                        header,
                        body,
                        ft.Divider(),
                        footer,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                width=self.CONTENT_WIDTH,
                height=self.CONTENT_HEIGHT,
                padding=30,
            ),
        )

    def cancel_clicked(self, e):
        e.page.go('/login')

    def prev_clicked(self, e):
        e.page.go('/set_vm_cpu_memory')

    def apply_clicked(self, e):
        job_id = AWXApiHelper.set_vm_cpu_memory(
            uri_base=self.session.get('awx_url'),
            loginid=self.session.get('awx_loginid'),
            password=self.session.get('awx_password'),
            job_template_name=self.JOB_TEMPLATE_NAME,
            parameter_dict={
                'vsphere_cluster': self.session.get('vsphere_cluster'),
                'target_vms': self.session.get('target_vms'),
                'vcpus': str(self.session.get('vcpus')),
                # 'memory_gb': self.session.get('memory_gb'),
                # 'reboot_before_change': self.checkShutdownBeforeChange.value,
                # 'startup_after_change': self.checkStartupAfterChange.value,
            },
        )
        if job_id > 0:
            self.session.set('job_id', job_id)
            e.page.go('/job_progress')
        else:
            print('job start failed!!!')
