from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.metrics import dp

from functions.setting_function import SettingFunctions

class SettingUI:
    def __init__(self, main_ui=None):
        """初始化設置 UI"""
        self.main_ui = main_ui
        self.setting_function = SettingFunctions()
        
        # 如果主 UI 存在，則從主 UI 同步設置
        if main_ui:
            try:
                self.setting_function.game_level = getattr(main_ui, 'game_level', 5)
                self.setting_function.game_questions = getattr(main_ui, 'game_questions', 10)
            except AttributeError:
                # 如果主 UI 沒有相關屬性，使用預設值
                self.setting_function.game_level = 5
                self.setting_function.game_questions = 10
            
        self.popup = None
        self.level_spinner = None
        self.count_spinner = None
        
    def show_settings(self, instance=None):
        """顯示設置彈出視窗"""
        # 獲取可用的難度選項和單詞數量統計
        level_options, level_counts = self.setting_function.get_available_levels()
        
        # 獲取可用的題數選項
        count_options = self.setting_function.get_available_question_counts(level_counts)
        
        # 驗證當前設置，確保在可用選項中
        current_level_text, current_count_text = self.setting_function.validate_current_settings(
            level_options, count_options
        )
        
        # 定義下拉選單的顏色（用於保持一致性）
        spinner_bg_color = (0.4, 0.5, 0.9, 1)
        
        # 創建浮動佈局作為根佈局
        root_layout = FloatLayout()
        
        # 建立垂直佈局來放置選項
        box_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(12),
            padding=dp(20),
            size_hint=(None, None),
            width=dp(280),
            height=dp(250),  # 縮小高度
            pos_hint={'center_x': 0.5, 'top': 0.9}  # 將選項容器移至標題下方
        )
        
        # 難度選擇下拉式選單
        level_label = Label(
            text="選擇難度:",
            font_name="NotoSansTC",
            font_size=dp(20),
            size_hint=(1, None),
            height=dp(30),
            halign='left'
        )
        box_layout.add_widget(level_label)
        
        self.level_spinner = Spinner(
            text=current_level_text,  # 使用當前/有效的難度
            values=level_options,
            font_name="NotoSansTC",
            font_size=dp(20),
            size_hint=(1, None),
            height=dp(40),
            background_color=spinner_bg_color,
            option_cls=SpinnerOption
        )
        box_layout.add_widget(self.level_spinner)
        
        # 題數選擇下拉式選單
        count_label = Label(
            text="選擇題數:",
            font_name="NotoSansTC",
            font_size=dp(20),
            size_hint=(1, None),
            height=dp(30),
            halign='left'
        )
        box_layout.add_widget(count_label)
        
        self.count_spinner = Spinner(
            text=current_count_text,  # 使用當前/有效的題數
            values=count_options,
            font_name="NotoSansTC",
            font_size=dp(20),
            size_hint=(1, None),
            height=dp(40),
            background_color=spinner_bg_color,
            option_cls=SpinnerOption
        )
        box_layout.add_widget(self.count_spinner)
        
        # 空間填充
        spacer = BoxLayout(size_hint=(1, None), height=dp(20))
        box_layout.add_widget(spacer)
        
        # 確定按鈕
        confirm_button = Button(
            text="確定",
            font_name="NotoSansTC",
            font_size=dp(20),
            size_hint=(None, None),
            size=(dp(100), dp(40)),  # 調整按鈕大小
            pos_hint={'center_x': 0.5},
            background_color=(0.2, 0.7, 0.2, 1)
        )
        box_layout.add_widget(confirm_button)
        
        # 將選項佈局添加到根佈局
        root_layout.add_widget(box_layout)
        
        # 創建彈出視窗
        self.popup = Popup(
            title="",
            content=root_layout,
            size_hint=(None, None),  # 使用固定大小
            size=(dp(320), dp(350)),  # 縮小整體尺寸
            separator_height=0,  # 去除分隔線
            background_color=(0.18, 0.18, 0.25, 1),  # 與其他彈出視窗保持一致的背景色
            auto_dismiss=True  # 允許點擊外部關閉
        )
        
        # 綁定確定按鈕事件
        confirm_button.bind(on_press=self.save_settings)
        
        # 顯示設置視窗
        self.popup.open()
    
    def save_settings(self, instance):
        """保存設置並關閉彈出視窗"""
        # 使用設置功能類保存設置
        level, question_count = self.setting_function.save_settings(
            self.level_spinner.text, 
            self.count_spinner.text
        )
        
        # 更新主 UI 中的設置
        if self.main_ui:
            self.main_ui.game_level = level
            self.main_ui.game_questions = question_count
        
        # 關閉彈出視窗
        self.popup.dismiss()


# 自定義下拉選項類，用於統一下拉選單顏色
class SpinnerOption(Button):
    def __init__(self, **kwargs):
        super(SpinnerOption, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0.4, 0.5, 0.9, 1)  # 與spinner_bg_color相同的顏色
        self.height = dp(35)
        self.font_name = "NotoSansTC"
        self.color = (1, 1, 1, 1)  # 確保文字顏色為白色 