# lock_total.py
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.utils import platform
from kivy.clock import Clock

PIN_OK = "123"

class LockScreen(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # layar hitam total
        Window.clearcolor = (0, 0, 0, 1)
        # PIN input
        self.pin = TextInput(
            password=True,
            font_size='60sp',
            size_hint=(None, None),
            width='250dp',
            height='90dp',
            pos_hint={'center_x': .5, 'center_y': .5},
            multiline=False
        )
        self.pin.bind(on_text_validate=self.cek)
        self.add_widget(self.pin)

    def cek(self, _):
        if self.pin.text == PIN_OK:
            App.get_running_app().stop()
        else:
            self.pin.text = ""           # reset jika salah

class LockApp(App):
    def build(self):
        Window.fullscreen = True
        return LockScreen()

    def on_start(self):
        if platform != 'android':
            return
        from jnius import autoclass
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        activity   = PythonActivity.mActivity
        View       = autoclass('android.view.View')
        decor      = activity.getWindow().getDecorView()
        # blokir semua kontrol sistem
        decor.setSystemUiVisibility(
            View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
            | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
            | View.SYSTEM_UI_FLAG_FULLSCREEN
            | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
            | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
            | View.SYSTEM_UI_FLAG_LAYOUT_STABLE
        )

    def on_pause(self):
        return True          # cegah masuk background

if __name__ == '__main__':
    LockApp().run()
