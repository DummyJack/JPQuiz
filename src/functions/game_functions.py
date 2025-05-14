import random
from database.db_manager import DBManager

class GameFunctions:
    def __init__(self):
        self.current_question = 0
        self.total_questions = 10
        self.correct_answers = 0
        self.db_manager = DBManager()
        self.correct_index = 0
        
    def reset_game(self):
        """重置遊戲狀態"""
        self.current_question = 0
        self.correct_answers = 0
        return self.current_question, self.total_questions
    
    def load_question(self):
        """載入新問題"""
        if self.current_question < self.total_questions:
            # 從資料庫獲取問題
            question_data = self.db_manager.get_random_word()
            
            if not question_data:
                # 如果沒有獲取到數據，使用預設數據
                question_data = {
                    "word": "日本語",
                    "options": ["日本語", "英語", "中国語", "韓国語"],
                    "correct_index": 0
                }
            
            # 更新問題和選項
            word = question_data["word"]
            
            # 打亂選項
            options = question_data["options"].copy()
            correct_option = options[question_data["correct_index"]]
            random.shuffle(options)
            
            # 更新正確答案的索引
            self.correct_index = options.index(correct_option)
            
            self.current_question += 1
            
            return word, options, self.correct_index
        else:
            return None, None, None
    
    def check_answer(self, selected_index):
        """檢查答案是否正確"""
        is_correct = False
        
        if selected_index == self.correct_index:
            # 答案正確
            is_correct = True
            self.correct_answers += 1
        
        return is_correct, self.correct_index
    
    def get_results(self):
        """獲取遊戲結果"""
        return self.correct_answers, self.total_questions
    
    def is_game_over(self):
        """檢查遊戲是否結束"""
        return self.current_question >= self.total_questions 