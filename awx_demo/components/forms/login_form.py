import flet as ft

from awx_demo.components.compounds.app_title import AppTitle
from awx_demo.components.compounds.parameter_input_text import ParameterInputText
from awx_demo.awx_api.awx_api_helper import AWXApiHelper


class LoginForm(ft.UserControl):
    """Login フォーム"""

    # const
    CONTENT_HEIGHT = 500
    CONTENT_WIDTH = 700
    BODY_HEIGHT = 250

    def __init__(self, session, page: ft.Page, default_awx_url):
        self.session = session
        self.page = page
        self.default_awx_url = default_awx_url
        self.dlgAuthFailed = ft.AlertDialog(
            modal=True,
            title=ft.Text('ログイン失敗'),
            content=ft.Text('認証に失敗しました。ログインIDとパスワードを確認して下さい。'),
            actions=[
                ft.TextButton('OK', on_click=self.close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        super().__init__()

    def build(self):
        self.tfLoginid = ParameterInputText(label='Login ID')
        self.tfPassword = ParameterInputText(
            label='Password', is_password=True)
        self.tfAWXUrl = ParameterInputText(
            label='AWX URL',
            value=self.session.get('awx_url') if self.session.contains_key(
                'awx_url') else self.default_awx_url,
        )
        self.btnLogin = ft.FilledButton(
            'ログイン', on_click=self.login_clicked)

        header = AppTitle(title='AWX API Demo', width=self.CONTENT_WIDTH)
        body = ft.Column(
            [
                self.tfLoginid,
                self.tfPassword,
                self.tfAWXUrl,
            ],
            height=self.BODY_HEIGHT,
        )
        footer = ft.Row(
            [
                self.btnLogin,
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

    def login_clicked(self, e):
        loginid = self.tfLoginid.value
        password = self.tfPassword.value
        awx_url = self.tfAWXUrl.value
        if self.login_auth(awx_url, loginid, password):
            self.session.set('awx_loginid', loginid)
            self.session.set('awx_password', password)
            self.session.set('awx_url', awx_url)
            e.page.go('/create_request')

    def close_dlg(self, e):
        self.dlgAuthFailed.open = False
        self.page.update()

    def open_dlg(self):
        self.page.dialog = self.dlgAuthFailed
        self.dlgAuthFailed.open = True
        self.page.update()

    def login_auth(self, awx_url, loginid, password):
        login_result = AWXApiHelper.login(awx_url, loginid, password)
        if not login_result:
            self.open_dlg()
        return login_result
