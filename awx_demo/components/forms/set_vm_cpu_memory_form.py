import flet as ft

from awx_demo.components.compounds.form_title import FormTitle
from awx_demo.components.compounds.form_description import FormDescription


class SetVmCpuMemoryForm(ft.UserControl):

    # const
    CONTENT_HEIGHT = 500
    CONTENT_WIDTH = 700
    BODY_HEIGHT = 250

    def __init__(self, session):
        self.session = session
        super().__init__()

    def build(self):
        formTitle = FormTitle('CPU/メモリの割り当て変更', '変更内容', self.CONTENT_WIDTH)
        formDescription = FormDescription('仮想マシンに割り当てるCPUコア数とメモリ容量を変更します。')
        self.textCpuslabel = ft.Text(
            value='CPUコア数: ' + str(self.session.get('vcpus')
                                   if self.session.contains_key('vcpus') else 2),
            style=ft.TextThemeStyle.BODY_SMALL,
            text_align=ft.TextAlign.LEFT,
        )
        self.sliderCpus = ft.Slider(
            value=self.session.get(
                'vcpus') if self.session.contains_key('vcpus') else 2,
            min=1,
            max=8,
            divisions=7,
            label='CPUコア数: {value}',
            on_change=self.slidercpus_changed,
        )
        self.dropMemorySize = ft.Dropdown(
            label='メモリ容量(GB)',
            value=self.session.get('memory_gb') if self.session.contains_key(
                'memory_gb') else 8,
            options=[
                ft.dropdown.Option(4),
                ft.dropdown.Option(8),
                ft.dropdown.Option(12),
                ft.dropdown.Option(16),
                ft.dropdown.Option(24),
                ft.dropdown.Option(32),
            ],
        )
        self.btnNext = ft.FilledButton(
            '次へ', on_click=self.next_clicked)
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
                self.textCpuslabel,
                self.sliderCpus,
                self.dropMemorySize,
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

    def slidercpus_changed(self, e):
        self.textCpuslabel.value = 'CPUコア数: ' + str(int(e.control.value))
        self.textCpuslabel.update()

    def cancel_clicked(self, e):
        e.page.go('/login')

    def prev_clicked(self, e):
        e.page.go('/select_target')

    def next_clicked(self, e):
        self.session.set('vcpus', int(self.sliderCpus.value))
        self.session.set('memory_gb', self.dropMemorySize.value)
        e.page.go('/set_vm_cpu_memory_confirm')
