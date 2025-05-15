# -*- coding: utf-8 -*-
import sys
import os

# 確保可以從任何位置導入模組
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_root)

# 嘗試導入，使用兼容的導入方式
try:
    from src.database.db_manager import DBManager
except ImportError:
    try:
        from database.db_manager import DBManager
    except ImportError:
        # 最後嘗試直接從腳本所在目錄的上級目錄導入
        sys.path.insert(0, os.path.dirname(current_dir))
        from database.db_manager import DBManager

import tabula
import pandas as pd

# 使用 os.path 來構建絕對路徑
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_FILE_PATH = os.path.join(BASE_DIR, 'resources', 'docs', 'N5.pdf')

def read_pdf_data(file_path):
    """讀取 PDF 文件中的表格數據"""
    if not os.path.exists(file_path):
        print(f"錯誤：找不到文件 '{file_path}'")
        print(f"當前工作目錄：{os.getcwd()}")
        print(f"檢查的完整路徑：{os.path.abspath(file_path)}")
        return []

    data = []
    try:
        dfs = tabula.read_pdf(
            file_path, 
            pages='all',
            lattice=True,
            pandas_options={'header': None}
        )
        
        for df in dfs:
            if len(df.columns) >= 2:
                for _, row in df.iterrows():
                    japanese = str(row[0]).strip()
                    meaning = str(row[1]).strip()
                    
                    if pd.notna(japanese) and pd.notna(meaning) and japanese != '' and meaning != '':
                        if not japanese.isdigit() and not meaning.isdigit():
                            data.append({
                                "japanese": japanese,
                                "level": 5,
                                "meaning": meaning
                            })
    except Exception as e:
        print(f"讀取 PDF 文件時發生錯誤: {e}")
        print(f"錯誤詳情: {str(e)}")
    return data

def insert_n5_data():
    """插入 N5 單字數據到 words collection"""
    data = read_pdf_data(DATA_FILE_PATH)
    success_count = 0
    
    if not data:
        print("沒有找到有效的數據")
        return

    # 獲取 MongoDB 連接
    db_manager = DBManager()
    
    try:
        # 確保 collection 存在
        collection = db_manager.crud.collection
        if db_manager.db is not None and collection is not None:
            for word in data:
                try:
                    # 檢查是否已存在相同單詞
                    existing = collection.find_one({"japanese": word["japanese"]})
                    if existing:
                        print(f"單詞已存在，跳過: {word['japanese']}")
                        continue
                        
                    # 插入數據到 words collection
                    result = collection.insert_one(word)
                    if result.inserted_id:
                        success_count += 1
                        print(f"成功插入: {word['japanese']} - {word['meaning']}")
                    else:
                        print(f"插入失敗: {word['japanese']} - {word['meaning']}")
                except Exception as e:
                    print(f"插入數據時發生錯誤: {word['japanese']} - {e}")
        else:
            print("無法連接到 MongoDB 或 collection 不存在")
    finally:
        db_manager.close_connection()
    
    print(f"\n總共成功插入 {success_count} 筆資料")

if __name__ == "__main__":
    insert_n5_data()