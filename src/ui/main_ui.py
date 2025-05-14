from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.metrics import dp

class MainUI(FloatLayout):
    def __init__(self, app=None, **kwargs):
        super(MainUI, self).__init__(**kwargs)
        self.app = app
        
        # 標題
        self.title = Label(
            text="日文學習益智遊戲",
            font_name="NotoSansTC",
            font_size=dp(36),
            size_hint=(1, 0.2),
            pos_hint={'top': 1, 'center_x': 0.5}
        )
        self.add_widget(self.title)
        
        # 遊戲開始按鈕
        self.start_button = Button(
            text="遊戲開始",
            font_name="NotoSansTC",
            font_size=dp(24),
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            background_color=(0.4, 0.5, 0.9, 1)
        )
        self.start_button.bind(on_press=self.start_game)
        self.add_widget(self.start_button)
        
        # 說明按鈕使用圖標
        self.help_button = Button(
            size_hint=(0.08, 0.05),
            pos_hint={'right': 0.98, 'top': 0.98},
            background_normal='help_icon.png',
            background_down='help_icon.png',
            border=(0, 0, 0, 0)
        )
        self.help_button.bind(on_press=self.show_help)
        self.add_widget(self.help_button)
        
        # 說明文字
        self.help_text = """
這是一個日文學習四選一益智遊戲。

遊戲說明：
1. 系統將從資料庫中隨機選取日文單字
2. 選擇正確的選項來回答問題
3. 總共有10題，答對越多分數越高
        """
        
        # 製作人資訊標籤（非按鈕）
        self.info_label = Label(
            text="製作人：JPQuiz開發團隊",
            font_name="NotoSansTC",
            font_size=dp(20),
            size_hint=(1, 0.08),
            pos_hint={'center_x': 0.5, 'y': 0},
            color=(1, 1, 1, 1)
        )
        self.add_widget(self.info_label)
    
    def start_game(self, instance):
        """開始遊戲"""
        if self.app:
            self.app.switch_to_game()
    
    def show_help(self, instance):
        """顯示遊戲說明"""
        popup = Popup(
            title="遊戲說明",
            title_font="NotoSansTC",
            content=Label(
                text=self.help_text,
                font_name="NotoSansTC"
            ),
            size_hint=(0.8, 0.6)
        )
        popup.open() 