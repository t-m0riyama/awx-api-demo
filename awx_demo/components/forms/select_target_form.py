import flet as ft

from awx_demo.components.compounds.parameter_input_text import ParameterInputText
from awx_demo.components.compounds.form_title import FormTitle
from awx_demo.components.compounds.form_description import FormDescription


class SelectTargetForm(ft.UserControl):

    # const
    CONTENT_HEIGHT = 500
    CONTENT_WIDTH = 700
    BODY_HEIGHT = 250

    def __init__(self, session):
        self.session = session
        super().__init__()

    def build(self):
        formTitle = FormTitle('変更対象の選択', 'クラスタと仮想マシンの指定', self.CONTENT_WIDTH)
        formDescription = FormDescription('変更対象の仮想マシンと稼働するクラスタを指定します。')
        self.dropCluster = ft.Dropdown(
            label='クラスタ',
            value=self.session.get('vsphere_cluster') if self.session.contains_key(
                'vsphere_cluster') else "cluster-1",
            options=[
                ft.dropdown.Option("cluster-1"),
                ft.dropdown.Option("cluster-99"),
            ],
            hint_text='仮想マシンの稼働するクラスタ名を指定します。',
        )
        self.tfVms = ParameterInputText(
            value=self.session.get('target_vms') if self.session.contains_key(
                'target_vms') else '',
            label='仮想マシン',
            hint_text='仮想マシンを指定します。複数の仮想マシンは、「,」で区切ることで指定できます。',
            on_change=self.tfVms_changed,
        )
        self.btnNext = ft.FilledButton(
            '次へ', on_click=self.next_clicked, disabled=True)
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
                self.dropCluster,
                self.tfVms,
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
        e.page.go('/create_request')

    def next_clicked(self, e):
        self.session.set('vsphere_cluster', self.dropCluster.value)
        self.session.set('target_vms', self.tfVms.value)
        e.page.go("/set_vm_cpu_memory")

    def tfVms_changed(self, e):
        if e.control.value == '':
            self.btnNext.disabled = True
        else:
            self.btnNext.disabled = False
        self.btnNext.update()
