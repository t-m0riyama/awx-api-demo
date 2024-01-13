import flet as ft


class ParameterInputText(ft.UserControl):

    def __init__(self, value=None, label='', hint_text='', is_password=False, on_change=None):
        self.tf = ft.TextField(
            value=value,
            label=label,
            autofocus=True,
            hint_text=hint_text,
            password=is_password,
            can_reveal_password=is_password,
            on_change=on_change)
        super().__init__()

    @property
    def value(self):
        return self.tf.value

    @value.setter
    def value(self, _value):
        self.tf.value = _value

    def build(self):
        return self.tf
