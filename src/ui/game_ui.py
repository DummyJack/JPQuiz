from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.animation import Animation

from functions.game_functions import GameFunctions

class GameUI(FloatLayout):
    def __init__(self, app=None, **kwargs):
        super(GameUI, self).__init__(**kwargs)
        self.app = app
        self.game_functions = GameFunctions()
        
        # 標題
        self.title = Label(
            text="資料庫中隨機選出一個單字",
            font_name="NotoSansTC",
            font_size=dp(24),
            size_hint=(1, 0.2),
            pos_hint={'top': 1, 'center_x': 0.5},
            color=(1, 1, 1, 1),
            opacity=0
        )
        self.add_widget(self.title)
        
        # 問題計數
        self.counter = Label(
            text="(總共 10 題)",
            font_name="NotoSansTC",
            font_size=dp(18),
            size_hint=(1, 0.1),
            pos_hint={'top': 0.85, 'center_x': 0.5},
            color=(1, 1, 1, 1),
            opacity=0
        )
        self.add_widget(self.counter)
        
        # 選項按鈕
        self.options_layout = GridLayout(
            cols=2,
            spacing=dp(10),
            padding=dp(20),
            size_hint=(0.8, 0.4),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            opacity=0
        )
        self.add_widget(self.options_layout)
        
        # 創建選項按鈕
        self.option_buttons = []
        for i in range(4):
            btn = Button(
                text=f"選項 {i+1}",
                font_name="NotoSansTC",
                font_size=dp(20),
                background_color=(0.4, 0.5, 0.9, 1)
            )
            btn.bind(on_press=self.check_answer)
            self.option_buttons.append(btn)
        
        # 返回主畫面按鈕
        self.back_button = Button(
            text="返回主畫面",
            font_name="NotoSansTC",
            font_size=dp(24),
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            background_color=(0.4, 0.5, 0.9, 1),
            opacity=0
        )
        self.back_button.bind(on_press=self.return_to_main)
        
        # 製作人資訊標籤（非按鈕）
        self.info_label = Label(
            text="製作人：JPQuiz開發團隊",
            font_name="NotoSansTC",
            font_size=dp(20),
            size_hint=(1, 0.08),
            pos_hint={'center_x': 0.5, 'y': 0},
            color=(1, 1, 1, 1),
            opacity=0
        )
        self.add_widget(self.info_label)
        
        # 初始狀態顯示選項
        self.show_options()
    
    def animate_elements(self):
        """為界面元素添加動畫效果"""
        # 清除所有動畫
        Animation.cancel_all(self.title)
        Animation.cancel_all(self.counter)
        Animation.cancel_all(self.options_layout)
        Animation.cancel_all(self.info_label)
        
        # 重設透明度
        self.title.opacity = 0
        self.counter.opacity = 0
        self.options_layout.opacity = 0
        self.info_label.opacity = 0
        
        # 標題動畫
        anim1 = Animation(opacity=1, duration=0.4)
        anim1.start(self.title)
        
        # 計數器動畫
        anim2 = Animation(opacity=0, duration=0) + Animation(opacity=1, duration=0.4, d=0.1)
        anim2.start(self.counter)
        
        # 選項按鈕動畫
        anim3 = Animation(opacity=0, duration=0) + Animation(opacity=1, duration=0.5, d=0.2)
        anim3.start(self.options_layout)
        
        # 資訊標籤動畫
        anim4 = Animation(opacity=0, duration=0) + Animation(opacity=1, duration=0.4, d=0.3)
        anim4.start(self.info_label)
        
    def reset_game(self):
        """重置遊戲狀態"""
        # 如果返回按鈕在界面上，先移除它
        if self.back_button.parent:
            self.remove_widget(self.back_button)
            
        # 更新標題
        self.title.text = "資料庫中隨機選出一個單字"
        
        # 使用功能類重置遊戲
        current_question, total_questions = self.game_functions.reset_game()
        self.update_counter(current_question, total_questions)
        
        # 確保選項按鈕可見
        self.show_options()
        
        # 播放動畫
        self.animate_elements()
        
        # 載入問題
        self.load_question()
    
    def show_options(self):
        """顯示選項按鈕"""
        # 清空選項佈局
        self.options_layout.clear_widgets()
        
        # 添加所有選項按鈕
        for btn in self.option_buttons:
            self.options_layout.add_widget(btn)
    
    def update_counter(self, current_question=0, total_questions=10):
        """更新問題計數器"""
        self.counter.text = f"(總共 {total_questions} 題)"
    
    def load_question(self):
        """載入新問題"""
        # 使用功能類載入問題
        word, options, correct_index = self.game_functions.load_question()
        
        if word is not None:
            # 更新問題和選項
            self.title.text = word
            
            # 設置選項按鈕
            for i, option in enumerate(options):
                self.option_buttons[i].text = option
                self.option_buttons[i].background_color = (0.4, 0.5, 0.9, 1)
        else:
            # 所有問題都完成了
            self.show_results()
    
    def check_answer(self, instance):
        """檢查答案是否正確"""
        selected_index = self.option_buttons.index(instance)
        
        # 使用功能類檢查答案
        is_correct, correct_index = self.game_functions.check_answer(selected_index)
        
        if is_correct:
            # 答案正確
            instance.background_color = (0.2, 0.8, 0.2, 1)  # 綠色
        else:
            # 答案錯誤
            instance.background_color = (0.8, 0.2, 0.2, 1)  # 紅色
            # 顯示正確答案
            self.option_buttons[correct_index].background_color = (0.2, 0.8, 0.2, 1)
        
        # 延遲加載下一個問題
        Clock.schedule_once(lambda dt: self.next_question(), 1.5)
    
    def next_question(self):
        """加載下一個問題或顯示結果"""
        if not self.game_functions.is_game_over():
            self.load_question()
        else:
            self.show_results()
    
    def show_results(self):
        """顯示遊戲結果"""
        # 使用功能類獲取結果
        correct_answers, total_questions = self.game_functions.get_results()
        
        # 顯示結果
        result_text = f"遊戲結束！\n正確答案: {correct_answers}/{total_questions}"
        self.title.text = result_text
        
        # 清空選項佈局
        self.options_layout.clear_widgets()
        
        # 顯示返回主畫面按鈕
        if not self.back_button.parent:
            # 重設按鈕透明度
            self.back_button.opacity = 0
            self.add_widget(self.back_button)
            # 添加淡入動畫
            anim = Animation(opacity=1, duration=0.5)
            anim.start(self.back_button)
    
    def return_to_main(self, instance):
        """返回主畫面"""
        if self.app:
            # 如果返回按鈕有父元素，則移除
            if self.back_button.parent:
                self.remove_widget(self.back_button)
            
            # 切換到主畫面
            self.app.switch_to_main() 