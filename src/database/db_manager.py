import pymongo

# 使用 try-except 兼容不同的導入路徑
try:
    # 當從主程式 (main.py) 導入時使用相對路徑
    from database.db_crud import DBCrud
except ImportError:
    # 當從腳本 (insert_n5_data.py) 導入時使用絕對路徑
    from src.database.db_crud import DBCrud

class DBManager:
    def __init__(self):
        """
        初始化資料庫管理器
        """
        try:
            # 連接到MongoDB，設置超時時間
            self.client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
            # 選擇資料庫
            self.db = self.client["jp_quiz_db"]
            
            # 檢查連接
            self.client.server_info()
            print("成功連接到 MongoDB")
            
            # 初始化CRUD操作類
            self.crud = DBCrud(self.db)
            
            # 初始化測試數據(如果集合為空)
            if len(self.crud.get_all_words()) <= 5:  # 只有測試數據時
                self.crud.initialize_test_data()
                
        except pymongo.errors.ServerSelectionTimeoutError:
            print("無法連接到 MongoDB")
            self.client = None
            self.db = None
            self.crud = DBCrud(None)  # 傳入None表示無法連接資料庫
    
    def get_all_words(self):
        """獲取所有單詞"""
        return self.crud.get_all_words()
    
    def get_words_by_level(self, level=5):
        """根據難度級別獲取單詞"""
        return self.crud.get_words_by_level(level)
    
    def count_words_by_level(self):
        """統計每個難度級別的單詞數量"""
        return self.crud.count_words_by_level()
    
    def get_random_words(self, count=10):
        """從資料庫中隨機獲取指定數量的單詞"""
        return self.crud.get_random_words(count)
    
    def save_log(self, log_data):
        """保存遊戲日誌到日誌集合"""
        return self.crud.save_log(log_data)
    
    def get_all_logs(self):
        """獲取所有日誌記錄"""
        return self.crud.get_all_logs()
    
    def get_log_by_id(self, log_id):
        """根據ID獲取特定日誌記錄"""
        return self.crud.get_log_by_id(log_id)
    
    def close_connection(self):
        """關閉與MongoDB的連接"""
        if self.client is not None:
            self.client.close()
            print("已關閉與MongoDB的連接")