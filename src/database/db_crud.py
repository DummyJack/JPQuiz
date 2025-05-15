import pymongo
import random
from datetime import datetime
from bson.objectid import ObjectId


class DBCrud:
    def __init__(self, db):
        """初始化數據庫操作類"""
        self.db = db
        if db is not None:
            self.collection = db["words"]
            self.log_collection = db["logs"]
        else:
            self.collection = None
            self.log_collection = None

    def initialize_test_data(self):
        """初始化測試數據"""
        test_data = [
            {"japanese": "こんにちは", "level": 5, "meaning": "你好（白天使用）"},
            {"japanese": "ありがとう", "level": 5, "meaning": "謝謝"},
            {"japanese": "さようなら", "level": 5, "meaning": "再見"},
            {"japanese": "おはよう", "level": 5, "meaning": "早安"},
            {"japanese": "すみません", "level": 5, "meaning": "對不起；不好意思"},
            {"japanese": "いただきます", "level": 5, "meaning": "開動前的感謝用語"},
            {"japanese": "おやすみなさい", "level": 5, "meaning": "晚安"},
            {"japanese": "はじめまして", "level": 5, "meaning": "初次見面"},
            {"japanese": "お爺さん", "level": 5, "meaning": "爺爺"},
            {"japanese": "おばあさん", "level": 5, "meaning": "奶奶"},
        ]

        # 插入測試數據
        if self.collection is not None:
            self.collection.insert_many(test_data)
            print(f"已初始化 {len(test_data)} 條測試數據")

    def get_all_words(self):
        """獲取所有單詞"""
        words = list(self.collection.find({}))

        return words

    def get_words_by_level(self, level=5):
        """根據難度級別獲取單詞"""
        if self.collection is None:
            print("無法獲取單詞：資料庫連接未建立")
            return []
            
        # 查詢指定難度的單詞
        words = list(self.collection.find({"level": level}))
        return words
    
    def count_words_by_level(self):
        """統計每個難度級別的單詞數量"""
        if self.collection is None:
            print("無法統計單詞：資料庫連接未建立")
            return {}
            
        # 使用聚合函數統計每個難度的單詞數量
        pipeline = [
            {"$group": {"_id": "$level", "count": {"$sum": 1}}}
        ]
        
        results = list(self.collection.aggregate(pipeline))
        
        # 將結果轉換為字典格式
        level_counts = {}
        for result in results:
            level_counts[result["_id"]] = result["count"]
            
        return level_counts

    def get_random_words(self, count=10):
        """從資料庫中隨機獲取指定數量的單詞"""

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
            obj_id = ObjectId(log_id)

            log = self.log_collection.find_one({"_id": obj_id})
            if log:
                log["_id"] = str(log["_id"])
            return log
        except Exception as e:
            print(f"獲取日誌時出錯：{e}")
            return None
