from kivy.app import App
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.resources import resource_add_path
import os

# 添加字體文件路徑
resource_add_path(os.path.abspath(os.path.dirname(__file__)))

# 註冊中文字體
LabelBase.register(name='NotoSansTC',
                  fn_regular='NotoSansTC-VariableFont_wght.ttf')

# Kivy UI 設計
KV = '''
#:set blue_color (0.259, 0.522, 0.957, 1)  # #4267B2
#:set info_color (0.357, 0.608, 0.835, 1)  # #5B9BD5

BoxLayout:
    orientation: 'vertical'
    padding: '20dp'
    spacing: '20dp'

    # 標題區域
    BoxLayout:
        size_hint_y: 0.2
        orientation: 'horizontal'
        spacing: '10dp'

        Label:
            text: '日語測驗'
            font_name: 'NotoSansTC'
            font_size: '24sp'
            size_hint_x: 0.8
            halign: 'right'

        Button:
            text: '?'
            font_size: '18sp'
            size_hint: (None, None)
            size: '40dp', '40dp'
            on_release: app.show_help()

    # 中間空白區域
    Widget:
        size_hint_y: 0.3

    # 遊戲開始按鈕
    Button:
        text: '遊戲開始'
        font_name: 'NotoSansTC'
        font_size: '18sp'
        size_hint: (None, None)
        size: '200dp', '60dp'
        pos_hint: {'center_x': 0.5}
        background_color: blue_color
        on_release: app.start_game()

    # 中間空白區域
    Widget:
        size_hint_y: 0.3

    # 補充資訊
    BoxLayout:
        size_hint_y: 0.1
        canvas.before:
            Color:
                rgba: info_color
            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            text: '製作人: Cursor、書賢'
            font_name: 'NotoSansTC'
            font_size: '16sp'
'''

class JapaneseQuizApp(App):
    def build(self):
        # 設置窗口大小
        Window.size = (400, 500)
        return Builder.load_string(KV)

    def show_help(self):
        popup = Popup(
            title='說明',
            content=Label(
                text='這是一個日語測驗遊戲，\n點擊開始按鈕進行測驗。',
                font_name='NotoSansTC'
            ),
            size_hint=(None, None),
            size=(300, 200)
        )
        popup.open()

    def start_game(self):
        print("遊戲開始")

if __name__ == '__main__':
    JapaneseQuizApp().run()