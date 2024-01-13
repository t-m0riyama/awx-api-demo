import flet as ft

from awx_demo.components.compounds.form_title import FormTitle
from awx_demo.components.compounds.form_description import FormDescription


class CreateRequestForm(ft.UserControl):

    # const
    CONTENT_HEIGHT = 500
    CONTENT_WIDTH = 700
    BODY_HEIGHT = 250

    def __init__(self, session):
        self.session = session
        super().__init__()

    def build(self):
        formTitle = FormTitle('申請の追加', '申請項目の種類を選択', self.CONTENT_WIDTH)
        formDescription = FormDescription('新しく申請を作成します。')
        self.dropCategory = ft.Dropdown(
            label='種別',
            value=self.session.get('request_category') if self.session.contains_key(
                'request_category') else 'サーバ',
            options=[
                ft.dropdown.Option('サーバ'),
            ],
        )
        self.dropOperation = ft.Dropdown(
            label='申請項目',
            value=self.session.get('request_operation') if self.session.contains_key(
                'request_operation') else 'CPUコア/メモリ割り当て変更',
            options=[
                ft.dropdown.Option('CPUコア/メモリ割り当て変更'),
            ],
        )
        self.btnNext = ft.FilledButton(
            '次へ', on_click=self.next_clicked)
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
                self.dropCategory,
                self.dropOperation,
            ],
            height=self.BODY_HEIGHT,
        )
        footer = ft.Row(
            [
                self.btnCancel,
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

    def next_clicked(self, e):
        self.session.set('request_category', self.dropCategory.value)
        self.session.set('request_operation', self.dropOperation.value)
        e.page.go('/select_target')
