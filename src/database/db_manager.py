import pymongo
import random
from datetime import datetime

class DBManager:
    def __init__(self):
        """初始化資料庫連接"""
        try:
            # 連接到MongoDB，設置超時時間
            self.client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
            # 選擇資料庫
            self.db = self.client["jp_quiz_db"]
            # 選擇單詞集合
            self.collection = self.db["words"]
            # 選擇日誌集合
            self.log_collection = self.db["logs"]
            
            # 檢查連接
            self.client.server_info()
            print("成功連接到 MongoDB")
            
            # 初始化測試數據(如果集合為空)
            if self.collection.count_documents({}) == 0:
                self._initialize_test_data()
                
        except pymongo.errors.ServerSelectionTimeoutError:
            print("無法連接到 MongoDB")
            self.client = None
            self.db = None
            self.collection = None
            self.log_collection = None
            
    def _initialize_test_data(self):
        """初始化測試數據"""
        test_data = [
            {
                "japanese": "こんにちは",
                "level": 5,
                "meaning": "你好（白天使用）"
            },
            {
                "japanese": "ありがとう",
                "level": 5,
                "meaning": "謝謝"
            },
            {
                "japanese": "さようなら",
                "level": 5,
                "meaning": "再見"
            },
            {
                "japanese": "おはよう",
                "level": 5,
                "meaning": "早安"
            },
            {
                "japanese": "すみません",
                "level": 5,
                "meaning": "對不起；不好意思"
            },
            {
                "japanese": "いただきます",
                "level": 5,
                "meaning": "開動前的感謝用語"
            },
            {
                "japanese": "おやすみなさい",
                "level": 5,
                "meaning": "晚安"
            },
            {
                "japanese": "はじめまして",
                "level": 5,
                "meaning": "初次見面"
            },
            {
                "japanese": "お爺さん",
                "level": 5,
                "meaning": "爺爺"
            },
            {
                "japanese": "おばあさん",
                "level": 5,
                "meaning": "奶奶"
            }
        ]
        
        # 插入測試數據
        if self.collection is not None:
            self.collection.insert_many(test_data)
            print(f"已初始化 {len(test_data)} 條測試數據")
    
    def get_all_words(self):
        """獲取所有單詞"""
        if self.collection is None:
            return self._get_test_words()
        
        words = list(self.collection.find({}))
        if not words:
            return self._get_test_words()
        
        return words
    
    def get_random_words(self, count=10):
        """從資料庫中隨機獲取指定數量的單詞"""
        if self.collection is None:
            return self._get_test_words()[:count]
        
        # 獲取全部單詞
        all_words = list(self.collection.find({}))
        
        if len(all_words) <= count:
            return all_words
        
        # 隨機選擇指定數量的單詞
        return random.sample(all_words, count)
    
    def save_log(self, log_data):
        """保存遊戲日誌到日誌集合"""
        if self.log_collection is None:
            print("無法保存日誌：資料庫連接未建立")
            return None
        
        # 確保時間戳格式正確
        if isinstance(log_data.get("timestamp"), str):
            try:
                log_data["timestamp"] = datetime.fromisoformat(log_data["timestamp"])
            except ValueError:
                log_data["timestamp"] = datetime.now()
        
        # 插入日誌記錄
        result = self.log_collection.insert_one(log_data)
        return str(result.inserted_id)
    
    def get_all_logs(self):
        """獲取所有日誌記錄"""
        if self.log_collection is None:
            print("無法獲取日誌：資料庫連接未建立")
            return []
        
        logs = list(self.log_collection.find().sort("timestamp", pymongo.DESCENDING))
        
        # 將MongoDB的ObjectId轉換為字符串
        for log in logs:
            log["_id"] = str(log["_id"])
        
        return logs
    
    def get_log_by_id(self, log_id):
        """根據ID獲取特定日誌記錄"""
        if self.log_collection is None:
            print("無法獲取日誌：資料庫連接未建立")
            return None
        
        try:
            # 將字符串ID轉換回ObjectId
            from bson.objectid import ObjectId
            obj_id = ObjectId(log_id)
            
            log = self.log_collection.find_one({"_id": obj_id})
            if log:
                log["_id"] = str(log["_id"])
            return log
        except Exception as e:
            print(f"獲取日誌時出錯：{e}")
            return None
    
    def close_connection(self):
        """關閉資料庫連接"""
        if self.client is not None:
            self.client.close()
            print("已關閉 MongoDB 連接")