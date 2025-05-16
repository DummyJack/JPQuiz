from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout  # 新增匯入BoxLayout用於漢字和假名排列

from functions.game_function import GameFunctions
from functions.log_function import LogFunctions

class GameUI(FloatLayout):
    def __init__(self, app=None, **kwargs):
        super(GameUI, self).__init__(**kwargs)
        self.app = app
        self.game_function = GameFunctions()
        self.log_function = LogFunctions()
        self.answer_selected = False  # 標記是否已選擇答案
        self.game_logged = False  # 標記是否已記錄遊戲結果
        
        # 問題計數 (新位置)
        self.counter = Label(
            text="第 1 題 / 10 題",
            font_name="NotoSansTC",
            font_size=dp(18),
            size_hint=(1, 0.1),
            pos_hint={'top': 1, 'center_x': 0.5},
            color=(1, 1, 1, 1),
            opacity=0
        )
        self.add_widget(self.counter)
        
        # 漢字標題 (新位置)
        self.title = Label(
            text="資料庫中隨機選出一個單字",
            font_name="NotoSansTC",
            font_size=dp(32),  # 字體放大
            size_hint=(1, 0.2),
            pos_hint={'top': 0.9, 'center_x': 0.5},
            color=(1, 1, 1, 1),
            opacity=0
        )
        self.add_widget(self.title)
        
        # 假名標籤，位於漢字上方
        self.furigana = Label(
            text="",
            font_name="NotoSansTC",
            font_size=dp(20),  # 假名字體較小
            size_hint=(1, 0.1),
            pos_hint={'bottom': 0.9, 'center_x': 0.5},  # 放置在漢字標題上方
            color=(0.9, 0.9, 1, 1),  # 稍微淺色
            opacity=0
        )
        self.add_widget(self.furigana)
        
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
                background_color=(0.4, 0.5, 0.9, 1),
                text_size=(dp(200), None),  # 設定文字區域寬度，高度自動調整
                halign='center',            # 水平居中對齊
                valign='middle',            # 垂直居中對齊
                padding_x=dp(10),           # 文字左右內邊距
                padding_y=dp(5),            # 文字上下內邊距
                line_height=1.2             # 行高，提高可讀性
            )
            btn.bind(on_press=self.check_answer)
            self.option_buttons.append(btn)
        
        # 返回主畫面按鈕 (使用圖標，位於左上角，縮小)
        self.back_button = Button(
            background_normal='back.png',
            background_down='back.png',
            border=(0, 0, 0, 0),
            size_hint=(0.08, 0.06),  # 縮小圖標尺寸
            pos_hint={'x': 0.02, 'top': 0.98},
            opacity=0
        )
        self.back_button.bind(on_press=self.return_to_main)
        self.add_widget(self.back_button)
        
        # 初始狀態顯示選項
        self.show_options()
    
    def animate_elements(self):
        """為界面元素添加動畫效果"""
        # 清除所有動畫
        Animation.cancel_all(self.title)
        Animation.cancel_all(self.furigana)  # 加入對假名的動畫控制
        Animation.cancel_all(self.counter)
        Animation.cancel_all(self.options_layout)
        Animation.cancel_all(self.back_button)
        
        # 重設透明度
        self.title.opacity = 0
        self.furigana.opacity = 0  # 設置假名透明度
        self.counter.opacity = 0
        self.options_layout.opacity = 0
        
        # 計數器動畫 (先於標題)
        anim1 = Animation(opacity=1, duration=0.4)
        anim1.start(self.counter)
        
        # 假名動畫
        anim_furigana = Animation(opacity=0, duration=0) + Animation(opacity=1, duration=0.4, d=0.1)
        anim_furigana.start(self.furigana)
        
        # 標題動畫
        anim2 = Animation(opacity=0, duration=0) + Animation(opacity=1, duration=0.4, d=0.1)
        anim2.start(self.title)
        
        # 選項按鈕動畫
        anim3 = Animation(opacity=0, duration=0) + Animation(opacity=1, duration=0.5, d=0.2)
        anim3.start(self.options_layout)
        
        # 返回按鈕動畫
        anim4 = Animation(opacity=1, duration=0.4)
        anim4.start(self.back_button)
    
    def reset_game_with_params(self, level=5, question_count=10):
        """使用指定參數重置遊戲狀態"""
        # 重設答案選擇狀態
        self.answer_selected = False
        self.game_logged = False
        
        # 更新標題
        self.title.text = "資料庫中隨機選出一個單字"
        self.furigana.text = ""  # 清空假名
        
        # 恢復標題原始位置和字體大小
        self.title.pos_hint = {'top': 0.9, 'center_x': 0.5}
        self.title.font_size = dp(32)
        self.title.color = (1, 1, 1, 1)  # 恢復原始顏色
        
        # 使用功能類重置遊戲，並傳入難度和題數
        current_question, total_questions = self.game_function.reset_game(level, question_count)
        self.update_counter(current_question + 1, total_questions)  # +1 因為題號從1開始顯示
        
        # 確保選項按鈕可見
        self.show_options()
        
        # 確保計數顯示
        self.counter.opacity = 1
        
        # 播放動畫
        self.animate_elements()
        
        # 載入問題
        self.load_question()
        
    def reset_game(self):
        """重置遊戲狀態（使用預設值）"""
        self.reset_game_with_params(5, 10)
    
    def show_options(self):
        """顯示選項按鈕"""
        # 清空選項佈局
        self.options_layout.clear_widgets()
        
        # 添加所有選項按鈕
        for btn in self.option_buttons:
            self.options_layout.add_widget(btn)
    
    def update_counter(self, current_question=1, total_questions=10):
        """更新問題計數器，顯示當前題號"""
        self.counter.text = f"第 {current_question} 題 / {total_questions} 題"
    
    def load_question(self):
        """載入新問題"""
        # 重設答案選擇狀態
        self.answer_selected = False
        
        # 使用功能類載入問題
        word, options, correct_index = self.game_function.load_question()
        
        if word is not None:
            # 解析問題（假設格式為「漢字[假名]」）
            if '[' in word and ']' in word:
                kanji_part = word.split('[')[0].strip()
                furigana_part = word.split('[')[1].split(']')[0].strip()
                
                # 更新漢字和假名標籤
                self.title.text = kanji_part
                self.furigana.text = furigana_part
            else:
                # 如果沒有假名標記，則整個問題顯示在標題中
                self.title.text = word
                self.furigana.text = ""
            
            # 更新問題計數器
            self.update_counter(self.game_function.current_question, self.game_function.total_questions)
            
            # 設置選項按鈕
            for i, option in enumerate(options):
                self.option_buttons[i].text = option
                self.option_buttons[i].background_color = (0.4, 0.5, 0.9, 1)  # 重設按鈕顏色
                self.option_buttons[i].disabled = False  # 啟用所有按鈕
        else:
            # 所有問題都完成了
            self.show_results()
    
    def check_answer(self, instance):
        """檢查答案是否正確"""
        # 如果已經選擇了答案，忽略此次點擊
        if self.answer_selected:
            return
            
        # 標記已選擇答案
        self.answer_selected = True
        
        # 禁用所有選項按鈕
        for btn in self.option_buttons:
            btn.disabled = True
        
        selected_index = self.option_buttons.index(instance)
        
        # 使用功能類檢查答案
        is_correct, correct_index = self.game_function.check_answer(selected_index)
        
        if is_correct:
            # 答案正確
            instance.background_color = (0.2, 0.8, 0.2, 1)  # 綠色
        else:
            # 答案錯誤
            instance.background_color = (0.8, 0.2, 0.2, 1)  # 紅色
            # 顯示正確答案
            self.option_buttons[correct_index].background_color = (0.2, 0.8, 0.2, 1)
        
        # 延遲加載下一個問題
        Clock.schedule_once(lambda dt: self.next_question(), 0.5)
    
    def next_question(self):
        """加載下一個問題或顯示結果"""
        if not self.game_function.is_game_over():
            self.load_question()
        else:
            self.show_results()
    
    def show_results(self):
        """顯示遊戲結果"""
        # 使用功能類獲取結果
        correct_answers, total_questions = self.game_function.get_results()
        
        # 隱藏問題計數器和假名標籤
        self.counter.opacity = 0
        self.furigana.opacity = 0
        
        # 清空選項佈局
        self.options_layout.clear_widgets()
        
        # 顯示結果，使用大膽的顏色和更大的字體
        result_text = f"    遊戲結束！\n正確答案: {correct_answers}/{total_questions}"
        self.title.text = result_text
        self.title.font_size = dp(40)  # 更大的字體
        self.title.pos_hint = {'center_x': 0.5, 'center_y': 0.5}  # 置中並稍微往右
        self.title.color = (1, 0.8, 0.2, 1)  # 明亮的金黃色
        
        # 保存遊戲日誌，確保只保存一次
        if not self.game_logged:
            self.game_function.save_game_log(self.log_function)
            self.game_logged = True
    
    def return_to_main(self, instance):
        """返回主畫面"""
        if self.app:
            # 切換到主畫面
            self.app.switch_to_main()