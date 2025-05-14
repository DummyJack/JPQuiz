import pymongo
from database.db_crud import DBCrud

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