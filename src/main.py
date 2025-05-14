from kivy.app import App
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.resources import resource_add_path
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.config import Config
import os

# 在程式開始前先設定視窗大小，避免啟動時的尺寸變化
Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '800')
Config.set('graphics', 'resizable', '0')  # 禁止調整大小
Config.write()  # 寫入配置

from ui.main_ui import MainUI
from ui.game_ui import GameUI

# 註冊字體 - 修正路徑到fonts目錄
resource_add_path(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources', 'fonts'))
resource_add_path(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources', 'icons'))
LabelBase.register(name='NotoSansTC', 
                  fn_regular='NotoSansTC-VariableFont_wght.ttf')

# 定義統一的背景色
BACKGROUND_COLOR = (0.15, 0.15, 0.2, 1)  # 深藍灰色

# 設置視窗背景色和位置
Window.clearcolor = BACKGROUND_COLOR
Window.position = 'custom'
Window.left = 100
Window.top = 100

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.ui = MainUI(app=App.get_running_app())
        self.add_widget(self.ui)
        
        # 添加背景
        with self.canvas.before:
            Color(*BACKGROUND_COLOR)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        
        # 綁定大小變化事件
        self.bind(size=self._update_rect, pos=self._update_rect)
    
    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.ui = GameUI(app=App.get_running_app())
        self.add_widget(self.ui)
        
        # 添加背景
        with self.canvas.before:
            Color(*BACKGROUND_COLOR)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        
        # 綁定大小變化事件
        self.bind(size=self._update_rect, pos=self._update_rect)
    
    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

class JPQuizApp(App):
    def build(self):
        # 創建屏幕管理器
        self.screen_manager = ScreenManager(transition=FadeTransition(duration=0.3))
        
        # 創建主屏幕和遊戲屏幕
        self.main_screen = MainScreen(name='main')
        self.game_screen = GameScreen(name='game')
        
        # 將屏幕添加到管理器
        self.screen_manager.add_widget(self.main_screen)
        self.screen_manager.add_widget(self.game_screen)
        
        # 初始化遊戲
        self.game_screen.ui.reset_game()
        
        # 返回主屏幕
        return self.screen_manager
    
    def switch_to_game(self):
        """切換到遊戲畫面"""
        self.game_screen.ui.reset_game()
        self.screen_manager.current = 'game'
    
    def switch_to_main(self):
        """返回主畫面"""
        self.screen_manager.current = 'main'

if __name__ == '__main__':
    JPQuizApp().run() 