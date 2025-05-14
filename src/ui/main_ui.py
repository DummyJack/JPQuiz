from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.animation import Animation

from ui.log_ui import LogUI

class MainUI(FloatLayout):
    def __init__(self, app=None, **kwargs):
        super(MainUI, self).__init__(**kwargs)
        self.app = app
        self.log_ui = LogUI()
        
        # 標題
        self.title = Label(
            text="日文學習益智遊戲",
            font_name="NotoSansTC",
            font_size=dp(36),
            size_hint=(1, 0.2),
            pos_hint={'top': 1, 'center_x': 0.5},
            color=(1, 1, 1, 1),
            opacity=0
        )
        self.add_widget(self.title)
        
        # 遊戲開始按鈕
        self.start_button = Button(
            text="遊戲開始",
            font_name="NotoSansTC",
            font_size=dp(24),
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.55},
            background_color=(0.4, 0.5, 0.9, 1),
            opacity=0
        )
        self.start_button.bind(on_press=self.start_game)
        self.add_widget(self.start_button)
        
        # 遊戲記錄按鈕
        self.log_button = Button(
            text="歷史記錄",
            font_name="NotoSansTC",
            font_size=dp(24),
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
            background_color=(0.4, 0.7, 0.7, 1),
            opacity=0
        )
        self.log_button.bind(on_press=self.log_ui.show_logs)
        self.add_widget(self.log_button)
        
        # 說明按鈕使用圖標
        self.help_button = Button(
            size_hint=(0.08, 0.05),
            pos_hint={'right': 0.98, 'top': 0.98},
            background_normal='help_icon.png',
            background_down='help_icon.png',
            border=(0, 0, 0, 0),
            opacity=0
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
            text="製作人：書賢、Cursor",
            font_name="NotoSansTC",
            font_size=dp(20),
            size_hint=(1, 0.08),
            pos_hint={'center_x': 0.5, 'y': 0},
            color=(1, 1, 1, 1),
            opacity=0
        )
        self.add_widget(self.info_label)
        
        # 添加漸入動畫
        self.schedule_animations()
    
    def schedule_animations(self):
        """安排元素的漸入動畫"""
        # 標題動畫
        anim1 = Animation(opacity=1, duration=0.5)
        anim1.start(self.title)
        
        # 開始按鈕動畫
        anim2 = Animation(opacity=0, duration=0) + Animation(opacity=1, duration=0.5, d=0.3)
        anim2.start(self.start_button)
        
        # 記錄按鈕動畫
        anim_log = Animation(opacity=0, duration=0) + Animation(opacity=1, duration=0.5, d=0.35)
        anim_log.start(self.log_button)
        
        # 幫助按鈕動畫
        anim3 = Animation(opacity=0, duration=0) + Animation(opacity=1, duration=0.5, d=0.4)
        anim3.start(self.help_button)
        
        # 資訊標籤動畫
        anim4 = Animation(opacity=0, duration=0) + Animation(opacity=1, duration=0.5, d=0.5)
        anim4.start(self.info_label)
    
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