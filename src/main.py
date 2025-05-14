from kivy.app import App
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.resources import resource_add_path
import os

from ui.main_ui import MainUI
from ui.game_ui import GameUI

# 註冊字體 - 修正路徑到fonts目錄
resource_add_path(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources', 'fonts'))
resource_add_path(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources', 'icons'))
LabelBase.register(name='NotoSansTC', 
                  fn_regular='NotoSansTC-VariableFont_wght.ttf')

class JPQuizApp(App):
    def build(self):
        # 設定視窗大小
        Window.size = (600, 800)
        
        # 設定主畫面
        self.main_ui = MainUI(app=self)
        self.game_ui = GameUI(app=self)
        
        # 初始化遊戲
        self.game_ui.reset_game()
        
        # 返回主畫面
        return self.main_ui
    
    def switch_to_game(self):
        """切換到遊戲畫面"""
        Window.remove_widget(self.main_ui)
        Window.add_widget(self.game_ui)
        self.game_ui.reset_game()
    
    def switch_to_main(self):
        """返回主畫面"""
        Window.remove_widget(self.game_ui)
        Window.add_widget(self.main_ui)

if __name__ == '__main__':
    JPQuizApp().run() 