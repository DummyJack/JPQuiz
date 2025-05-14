from datetime import datetime
from database.db_manager import DBManager

class LogFunctions:
    def __init__(self):
        """初始化日誌功能"""
        self.db_manager = DBManager()
    
    def save_game_log(self, level, questions, correct_answers, question_results):
        """
        保存遊戲記錄到資料庫
        
        參數:
        - level: 遊戲難度
        - questions: 問題列表
        - correct_answers: 答對題數
        - question_results: 每題的結果(正確/錯誤)列表
        """
        # 創建日誌記錄
        log_data = {
            "level": level,
            "total_questions": len(questions),
            "correct_answers": correct_answers,
            "timestamp": datetime.now(),
            "questions": []
        }
        
        # 添加每個問題的詳細記錄
        for i, question in enumerate(questions):
            log_data["questions"].append({
                "question_id": str(question.get("_id", i)),  # 使用MongoDB _id或fallback到索引
                "japanese": question.get("japanese", ""),
                "meaning": question.get("meaning", ""),
                "is_correct": question_results[i]
            })
        
        # 保存日誌
        return self.db_manager.save_log(log_data)
    
    def get_all_logs(self):
        """獲取所有遊戲記錄"""
        return self.db_manager.get_all_logs()
    
    def get_log_by_id(self, log_id):
        """根據ID獲取特定遊戲記錄"""
        return self.db_manager.get_log_by_id(log_id)
    
    def format_timestamp(self, timestamp, date_only=False):
        """格式化時間戳為可讀字符串
        
        參數:
        - timestamp: 時間戳
        - date_only: 是否只返回日期，不包含時間
        """
        if isinstance(timestamp, datetime):
            if date_only:
                return timestamp.strftime("%Y-%m-%d")
            else:
                return timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return str(timestamp)