from database.db_manager import DBManager

class SettingFunctions:
    def __init__(self):
        """初始化設置功能類"""
        self.db_manager = DBManager()
        # 遊戲設置預設值
        self.game_level = 5  # 預設難度 N5
        self.game_questions = 10  # 預設題數
    
    def get_available_levels(self):
        """獲取可用的難度選項"""
        # 獲取資料庫中所有單詞
        all_words = self.db_manager.get_all_words()
        
        # 統計每個難度等級的單詞數量
        level_counts = {}
        for word in all_words:
            level = word.get("level", 5)  # 預設為 N5
            if level not in level_counts:
                level_counts[level] = 0
            level_counts[level] += 1
        
        # 創建可用難度選項
        level_options = []
        for level in range(1, 6):  # N1-N5
            if level_counts.get(level, 0) >= 10:  # 至少有10個單詞
                level_text = f"N{level}"
                level_options.append(level_text)
        
        if not level_options:  # 確保至少有一個選項
            level_options = ["N5"]
            
        return level_options, level_counts
    
    def get_available_question_counts(self, level_counts):
        """獲取可用的題數選項"""
        # 創建可用題數選項
        count_options = []
        for count in [10, 15, 20]:
            max_level_count = max([level_counts.get(level, 0) for level in range(1, 6)])
            if max_level_count >= count:
                count_options.append(str(count))
        
        if not count_options:  # 確保至少有一個選項
            count_options = ["10"]
            
        return count_options
    
    def save_settings(self, level_text, count_text):
        """保存設置的難度和題數"""
        # 獲取選中的難度
        self.game_level = int(level_text[1])  # 從 "N5" 提取數字 5
        
        # 獲取選中的題數
        self.game_questions = int(count_text)
        
        return self.game_level, self.game_questions
    
    def get_current_settings(self):
        """獲取當前設置"""
        return {
            "level": self.game_level,
            "question_count": self.game_questions
        }
    
    def get_current_level_text(self):
        """獲取當前難度的文本表示"""
        return f"N{self.game_level}"
    
    def get_current_question_count_text(self):
        """獲取當前題數的文本表示"""
        return str(self.game_questions)
    
    def validate_current_settings(self, level_options, count_options):
        """驗證當前設置是否有效，返回有效的設置值"""
        # 檢查當前難度是否在可用選項中
        current_level_text = self.get_current_level_text()
        if current_level_text not in level_options:
            # 如果當前難度不可用，使用預設值(N5)或第一個可用選項
            current_level_text = "N5" if "N5" in level_options else level_options[0]
            self.game_level = int(current_level_text[1])
        
        # 檢查當前題數是否在可用選項中
        current_count_text = self.get_current_question_count_text()
        if current_count_text not in count_options:
            # 如果當前題數不可用，使用預設值(10)或第一個可用選項
            current_count_text = "10" if "10" in count_options else count_options[0]
            self.game_questions = int(current_count_text)
        
        return current_level_text, current_count_text 