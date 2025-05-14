import random
from database.db_manager import DBManager

class GameFunctions:
    def __init__(self):
        self.current_question = 0
        self.total_questions = 10
        self.correct_answers = 0
        self.db_manager = DBManager()
        self.correct_index = 0
        self.questions = []
        self.all_words = []
        self.questions_with_options = []  # 預先生成的問題和選項
        self.question_results = []  # 記錄每題的結果 (True: 正確, False: 錯誤)
        self.current_level = 5  # 預設難度等級
        
    def reset_game(self):
        """重置遊戲狀態並預先載入所有題目與選項"""
        self.current_question = 0
        self.correct_answers = 0
        self.question_results = []  # 清空結果記錄
        
        # 獲取所有單詞以便生成選項
        self.all_words = self.db_manager.get_all_words()
        
        # 獲取10個隨機問題
        self.questions = self.db_manager.get_random_words(10)
        
        # 預先處理所有問題和選項
        self.questions_with_options = []
        for question_data in self.questions:
            # 提取日文單詞和正確答案（中文意思）
            japanese_word = question_data["japanese"]
            correct_meaning = question_data["meaning"]
            
            # 設置當前等級
            self.current_level = question_data.get("level", 5)
            
            # 生成選項（包括正確答案和3個隨機錯誤答案）
            options = [correct_meaning]
            
            # 從所有單詞中選擇3個不同的錯誤選項
            other_meanings = [word["meaning"] for word in self.all_words 
                            if word["meaning"] != correct_meaning]
            
            # 如果可用的錯誤選項不足3個，則重複使用
            if len(other_meanings) < 3:
                other_meanings = other_meanings * 3
            
            # 隨機選擇3個錯誤選項
            wrong_options = random.sample(other_meanings, 3)
            options.extend(wrong_options)
            
            # 打亂選項順序
            random.shuffle(options)
            
            # 記錄正確答案的索引
            correct_index = options.index(correct_meaning)
            
            # 保存問題和選項
            self.questions_with_options.append({
                "japanese": japanese_word,
                "options": options,
                "correct_index": correct_index,
                "original_data": question_data  # 保存原始問題數據，包括_id
            })
        
        return self.current_question, self.total_questions
    
    def load_question(self):
        """載入新問題，直接使用預先生成的問題和選項"""
        if self.current_question < self.total_questions and self.current_question < len(self.questions_with_options):
            # 獲取當前問題數據
            question_data = self.questions_with_options[self.current_question]
            
            japanese_word = question_data["japanese"]
            options = question_data["options"]
            self.correct_index = question_data["correct_index"]
            
            self.current_question += 1
            
            return japanese_word, options, self.correct_index
        else:
            return None, None, None
    
    def check_answer(self, selected_index):
        """檢查答案是否正確"""
        is_correct = False
        
        if selected_index == self.correct_index:
            # 答案正確
            is_correct = True
            self.correct_answers += 1
        
        # 記錄答題結果
        self.question_results.append(is_correct)
        
        return is_correct, self.correct_index
    
    def get_results(self):
        """獲取遊戲結果"""
        return self.correct_answers, self.total_questions
    
    def is_game_over(self):
        """檢查遊戲是否結束"""
        return self.current_question >= self.total_questions or self.current_question >= len(self.questions_with_options)
    
    def get_log_data(self):
        """獲取日誌數據"""
        return {
            "level": self.current_level,
            "questions": self.questions,
            "correct_answers": self.correct_answers,
            "question_results": self.question_results
        }
    
    def get_question_details(self):
        """獲取問題詳細信息列表"""
        details = []
        for i, question_data in enumerate(self.questions_with_options):
            if i < len(self.question_results):  # 確保已經回答過這個問題
                original_data = question_data.get("original_data", {})
                details.append({
                    "question_id": str(original_data.get("_id", i)),
                    "japanese": question_data["japanese"],
                    "meaning": original_data.get("meaning", ""),
                    "is_correct": self.question_results[i]
                })
        return details