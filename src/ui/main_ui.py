from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

from ui.log_ui import LogUI
from ui.setting_ui import SettingUI
from database.db_manager import DBManager

class MainUI(FloatLayout):
    def __init__(self, app=None, **kwargs):
        super(MainUI, self).__init__(**kwargs)
        self.app = app
        self.log_ui = LogUI()
        self.db_manager = DBManager()
        
        # 遊戲設置
        self.game_level = 5  # 預設難度 N5
        self.game_questions = 10  # 預設題數
        
        # 初始化設置 UI（必須在設置遊戲參數後）
        self.setting_ui = SettingUI(self)
        
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
            pos_hint={'center_x': 0.5, 'center_y': 0.63},
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
            pos_hint={'center_x': 0.5, 'center_y': 0.48},
            background_color=(0.4, 0.7, 0.7, 1),
            opacity=0
        )
        self.log_button.bind(on_press=self.log_ui.show_logs)
        self.add_widget(self.log_button)
        
        # 設置按鈕
        self.settings_button = Button(
            text="設置",
            font_name="NotoSansTC",
            font_size=dp(24),
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.33},
            background_color=(0.75, 0.75, 0.75, 1),
            opacity=0
        )
        self.settings_button.bind(on_press=self.setting_ui.show_settings)
        self.add_widget(self.settings_button)
        
        # 說明按鈕使用圖標
        self.help_button = Button(
            size_hint=(0.08, 0.06),
            pos_hint={'right': 0.98, 'top': 0.97},
            background_normal='help_icon.png',
            background_down='help_icon.png',
            border=(0, 0, 0, 0),
            opacity=0
        )
        self.help_button.bind(on_press=self.show_help)
        self.add_widget(self.help_button)
        
        # 說明文字
        self.help_text = """
            1. 遊戲開始即可開始遊玩

            2. 點選歷史紀錄可以查看自己過去答題表現
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
        
        # 為 info_label 添加背景
        with self.info_label.canvas.before:
            Color(0.2, 0.2, 0.3, 1)  # 稍微比背景色淺一點的顏色
            self.info_bg = Rectangle(pos=self.info_label.pos, size=self.info_label.size)
        
        # 綁定事件以更新背景大小和位置
        self.info_label.bind(pos=self._update_info_bg, size=self._update_info_bg)
        
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
        
        # 設置按鈕動畫
        anim_settings = Animation(opacity=0, duration=0) + Animation(opacity=1, duration=0.5, d=0.4)
        anim_settings.start(self.settings_button)
        
        # 幫助按鈕動畫
        anim3 = Animation(opacity=0, duration=0) + Animation(opacity=1, duration=0.5, d=0.45)
        anim3.start(self.help_button)
        
        # 資訊標籤動畫
        anim4 = Animation(opacity=0, duration=0) + Animation(opacity=1, duration=0.5, d=0.5)
        anim4.start(self.info_label)
    
    def start_game(self, instance):
        """開始遊戲"""
        if self.app:
            # 設置遊戲參數
            self.app.set_game_params(self.game_level, self.game_questions)
            self.app.switch_to_game()
    
    def show_help(self, instance):
        """顯示遊戲說明"""
        # 創建浮動佈局作為彈出視窗的內容容器
        content_layout = FloatLayout()
        
        # 添加說明文字標籤
        content_label = Label(
            text=self.help_text,
            font_name="NotoSansTC",
            font_size=dp(18),
            pos_hint={'center_x': 0.4, 'top': 1.3},
        )
        content_layout.add_widget(content_label)
        
        # 創建自訂彈出視窗
        popup = Popup(
            title="遊戲說明",
            title_size=dp(24),  # 放大標題
            title_font="NotoSansTC",
            title_align="center",  # 標題置中
            content=content_layout,
            size_hint=(0.8, 0.6),
            separator_color=(0, 0, 0, 0),  # 去除藍色分隔線（設為透明）
            auto_dismiss=True  # 允許點擊外部關閉
        )
        
        # 添加關閉按鈕 (X)
        close_button = Button(
            text="X",
            size_hint=(0.1, 0.1),  # 稍微增加按鈕大小
            pos_hint={'right': 0.99, 'top': 1.13},  # 移到更靠近右上角
            background_color=(0.7, 0.7, 0.7, 1),  # 更改為淺灰色背景
            color=(1, 1, 1, 1)  # 白色文字
        )
        close_button.bind(on_press=popup.dismiss)  # 按下按鈕關閉彈出視窗
        content_layout.add_widget(close_button)
        
        popup.open()

    def _update_info_bg(self, instance, value):
        """更新信息標籤背景的大小和位置"""
        self.info_bg.pos = instance.pos
        self.info_bg.size = instance.size