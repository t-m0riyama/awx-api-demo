import flet as ft
from apscheduler.schedulers.background import BackgroundScheduler

from awx_demo.components.compounds.form_title import FormTitle
from awx_demo.components.compounds.form_description import FormDescription
from awx_demo.awx_api.awx_api_helper import AWXApiHelper


class JobProgressForm(ft.UserControl):

    # const
    CONTENT_HEIGHT = 500
    CONTENT_WIDTH = 700
    BODY_HEIGHT = 250
    JOB_STATUS_CHECK_ID = 'job_status_check'

    def __init__(self, session):
        self.session = session
        super().__init__()

    def build(self):
        formTitle = FormTitle('処理の進捗', 'ジョブの進捗状況', self.CONTENT_WIDTH)
        formDescription = FormDescription('ジョブの進捗状況を表示します。')
        self.pbJob = ft.ProgressBar(value=0, width=self.CONTENT_WIDTH)
        self.lvProgressLog = ft.ListView(
            # expand=1,
            spacing=10,
            padding=10,
            divider_thickness=1,
            auto_scroll=True)
        self.lvProgressLog.controls.append(
            ft.Row(
                [
                    ft.Icon(ft.icons.INFO_OUTLINED, color=ft.colors.BLUE_500),
                    ft.Text(
                        value='処理を開始しました。',
                        style=ft.TextThemeStyle.BODY_LARGE,
                        color=ft.colors.SECONDARY
                    ),
                ]
            )
        )
        self.btnExit = ft.FilledButton(
            '終了', on_click=self.exit_clicked, disabled=True)
        self.btnNewRequest = ft.ElevatedButton(
            '新しい申請の作成', on_click=self.new_request_clicked, disabled=True)

        # Content
        header = ft.Container(
            formTitle,
            margin=ft.margin.only(bottom=20),
        )
        body = ft.Column(
            [
                formDescription,
                self.pbJob,
                self.lvProgressLog,
            ],
            height=self.BODY_HEIGHT,
        )
        footer = ft.Row(
            [
                self.btnNewRequest,
                self.btnExit,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(
            self.refresh_progress, 'interval', seconds=3, id=self.JOB_STATUS_CHECK_ID)
        try:
            self.scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            pass

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

    def new_request_clicked(self, e):
        e.page.go('/create_request')

    def exit_clicked(self, e):
        e.page.go('/login')

    def refresh_progress(self):
        job_status = AWXApiHelper.get_job_status(
            uri_base=self.session.get('awx_url'),
            loginid=self.session.get('awx_loginid'),
            password=self.session.get('awx_password'),
            job_id=self.session.get('job_id'),
        )
        if job_status == 'successful':
            self.pbJob.value = 1.0
            try:
                self.scheduler.remove_job(self.JOB_STATUS_CHECK_ID)
                self.scheduler.pause()
            except (KeyboardInterrupt, SystemExit):
                pass
            self.lvProgressLog.controls.append(
                ft.Row(
                    [
                        ft.Icon(ft.icons.THUMB_UP_OUTLINED,
                                color=ft.colors.BLUE_500),
                        ft.Text(
                            value='処理は正常終了しました。',
                            style=ft.TextThemeStyle.BODY_LARGE,
                            color=ft.colors.SECONDARY
                        ),
                    ]
                )
            )
            self.lvProgressLog.controls.append(
                ft.TextButton(
                    'ジョブ出力の参照: ' +
                    self.session.get(
                        'awx_url') + '/#/jobs/playbook/{}/output'.format(self.session.get('job_id')),
                    url=self.session.get(
                        'awx_url') + '/#/jobs/playbook/{}/output'.format(self.session.get('job_id')),
                ),
            )
            self.btnExit.disabled = False
            self.btnNewRequest.disabled = False
            self.lvProgressLog.update()
            self.btnExit.update()
            self.btnNewRequest.update()
        elif job_status == 'failed':
            try:
                self.scheduler.remove_job(self.JOB_STATUS_CHECK_ID)
                self.scheduler.pause()
            except (KeyboardInterrupt, SystemExit):
                pass
            self.lvProgressLog.controls.append(
                ft.Row(
                    [
                        ft.Icon(ft.icons.ERROR_OUTLINED,
                                color=ft.colors.ERROR),
                        ft.Text(
                            value='処理に失敗しました。',
                            style=ft.TextThemeStyle.BODY_LARGE,
                            color=ft.colors.SECONDARY
                        ),
                    ]
                )
            )
            self.lvProgressLog.controls.append(
                ft.TextButton(
                    'ジョブ出力の参照: ' +
                    self.session.get(
                        'awx_url') + '/#/jobs/playbook/{}/output'.format(self.session.get('job_id')),
                    url=self.session.get(
                        'awx_url') + '/#/jobs/playbook/{}/output'.format(self.session.get('job_id')),
                ),
            )
            self.btnExit.disabled = False
            self.btnNewRequest.disabled = False
            self.lvProgressLog.update()
            self.btnExit.update()
            self.btnNewRequest.update()

        if job_status == 'running':
            if self.pbJob.value < 0.9:
                self.pbJob.value += 0.1
        self.pbJob.update()
