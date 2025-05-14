import pymongo
import random

class DBManager:
    def __init__(self):
        """初始化資料庫連接"""
        try:
            # 連接到MongoDB，設置超時時間
            self.client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
            # 選擇資料庫
            self.db = self.client["jp_quiz_db"]
            # 選擇集合 (collection)
            self.collection = self.db["words"]
            
            # 檢查連接
            self.client.server_info()
            print("成功連接到MongoDB")
            
            # 初始化測試數據(如果集合為空)
            if self.collection.count_documents({}) == 0:
                self._initialize_test_data()
                
        except pymongo.errors.ServerSelectionTimeoutError:
            print("無法連接到MongoDB - 使用測試數據")
            self.client = None
            self.db = None
            self.collection = None
            
    def _initialize_test_data(self):
        """初始化測試數據"""
        test_data = [
            {
                "word": "猫",
                "pronunciation": "ねこ (neko)",
                "meaning": "貓",
                "options": ["貓", "狗", "鳥", "魚"],
                "correct_index": 0
            },
            {
                "word": "犬",
                "pronunciation": "いぬ (inu)",
                "meaning": "狗",
                "options": ["貓", "狗", "鳥", "魚"],
                "correct_index": 1
            },
            {
                "word": "鳥",
                "pronunciation": "とり (tori)",
                "meaning": "鳥",
                "options": ["貓", "狗", "鳥", "魚"],
                "correct_index": 2
            },
            {
                "word": "魚",
                "pronunciation": "さかな (sakana)",
                "meaning": "魚",
                "options": ["貓", "狗", "鳥", "魚"],
                "correct_index": 3
            },
            {
                "word": "車",
                "pronunciation": "くるま (kuruma)",
                "meaning": "車",
                "options": ["車", "船", "飛機", "火車"],
                "correct_index": 0
            },
            {
                "word": "本",
                "pronunciation": "ほん (hon)",
                "meaning": "書",
                "options": ["書", "雜誌", "報紙", "筆記本"],
                "correct_index": 0
            },
            {
                "word": "水",
                "pronunciation": "みず (mizu)",
                "meaning": "水",
                "options": ["水", "火", "土", "風"],
                "correct_index": 0
            },
            {
                "word": "山",
                "pronunciation": "やま (yama)",
                "meaning": "山",
                "options": ["山", "河", "海", "湖"],
                "correct_index": 0
            },
            {
                "word": "林檎",
                "pronunciation": "りんご (ringo)",
                "meaning": "蘋果",
                "options": ["蘋果", "香蕉", "橙子", "梨"],
                "correct_index": 0
            },
            {
                "word": "学校",
                "pronunciation": "がっこう (gakkou)",
                "meaning": "學校",
                "options": ["學校", "醫院", "公園", "圖書館"],
                "correct_index": 0
            }
        ]
        
        # 插入測試數據
        if self.collection is not None:
            self.collection.insert_many(test_data)
            print(f"已初始化 {len(test_data)} 條測試數據")
    
    def get_random_word(self):
        """從資料庫中隨機獲取一個單詞"""
        if self.collection is None:
            # 如果沒有連接到資料庫，返回測試數據
            return self._get_test_word()
        
        # 計算集合中的文檔數量
        count = self.collection.count_documents({})
        if count == 0:
            return None
        
        # 隨機選擇一個索引
        random_index = random.randint(0, count - 1)
        
        # 獲取隨機文檔
        word_data = self.collection.find().limit(1).skip(random_index)
        
        try:
            word_doc = next(word_data)
            # 轉換ObjectId為字符串
            word_doc["_id"] = str(word_doc["_id"])
            return word_doc
        except StopIteration:
            return None
    
    def _get_test_word(self):
        """獲取預設測試單詞"""
        test_words = [
            {
                "word": "猫",
                "pronunciation": "ねこ (neko)",
                "meaning": "貓",
                "options": ["貓", "狗", "鳥", "魚"],
                "correct_index": 0
            },
            {
                "word": "犬",
                "pronunciation": "いぬ (inu)",
                "meaning": "狗",
                "options": ["貓", "狗", "鳥", "魚"],
                "correct_index": 1
            },
            {
                "word": "鳥",
                "pronunciation": "とり (tori)",
                "meaning": "鳥",
                "options": ["貓", "狗", "鳥", "魚"],
                "correct_index": 2
            },
            {
                "word": "魚",
                "pronunciation": "さかな (sakana)",
                "meaning": "魚",
                "options": ["貓", "狗", "鳥", "魚"],
                "correct_index": 3
            },
            {
                "word": "車",
                "pronunciation": "くるま (kuruma)",
                "meaning": "車",
                "options": ["車", "船", "飛機", "火車"],
                "correct_index": 0
            }
        ]
        
        return random.choice(test_words)
    
    def close_connection(self):
        """關閉資料庫連接"""
        if self.client is not None:
            self.client.close()
            print("已關閉MongoDB連接") 