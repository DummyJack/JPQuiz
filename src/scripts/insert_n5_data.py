# -*- coding: utf-8 -*-
import sys
import os
import tempfile
import logging
from pathlib import Path

# 設置日誌
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# 確保可以從任何位置導入模組
current_dir = Path(__file__).parent.absolute()
project_root = current_dir.parent.parent
sys.path.insert(0, str(project_root))

from src.database.db_manager import DBManager
import tabula
import pandas as pd

# 使用 Path 來構建絕對路徑
BASE_DIR = project_root
DATA_FILE_PATH = BASE_DIR / "resources" / "docs" / "N5.pdf"


def read_pdf_data(file_path):
    """從PDF文件中讀取表格數據並轉換為日文單詞字典列表"""
    file_path = Path(file_path)
    if not file_path.exists():
        logger.error(f"找不到文件: {file_path}")
        logger.info(f"當前工作目錄: {os.getcwd()}")
        logger.info(f"檢查的完整路徑: {file_path.absolute()}")
        return []

    data = []
    temp_path = None

    try:
        # 創建臨時CSV文件
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as temp_file:
            temp_path = temp_file.name

        # 將PDF轉換為CSV，避開JSON解析錯誤
        logger.info(f"正在轉換PDF文件: {file_path}")
        tabula.convert_into(
            str(file_path), temp_path, output_format="csv", pages="all", lattice=True
        )

        # 讀取並處理CSV數據
        try:
            df = pd.read_csv(temp_path, header=None, encoding="utf-8")
            logger.info(f"從CSV讀取到 {len(df)} 行數據")

            # 建立有效的單詞詞典列表
            for i in range(len(df)):
                if len(df.columns) < 2:
                    continue

                japanese = str(df.iloc[i, 0]).strip() if pd.notna(df.iloc[i, 0]) else ""
                meaning = str(df.iloc[i, 1]).strip() if pd.notna(df.iloc[i, 1]) else ""

                # 驗證單詞有效性
                if (
                    japanese
                    and meaning
                    and not japanese.isdigit()
                    and not meaning.isdigit()
                    and len(japanese) > 1
                    and japanese != "japanese"
                    and meaning != "meaning"
                ):

                    word_data = {"japanese": japanese, "level": 5, "meaning": meaning}
                    data.append(word_data)

                    if len(data) % 100 == 0:  # 每100個單詞記錄一次
                        logger.info(f"已處理 {len(data)} 個單詞")

            logger.info(f"總共解析出 {len(data)} 個有效單詞")
        except Exception as e:
            logger.error(f"讀取CSV文件時發生錯誤: {e}")

    except Exception as e:
        logger.error(f"處理PDF文件時發生錯誤: {str(e)}")

    finally:
        # 清理臨時文件
        if temp_path and Path(temp_path).exists():
            try:
                os.unlink(temp_path)
            except Exception as e:
                logger.warning(f"刪除臨時文件失敗: {e}")

    return data


def insert_n5_data():
    """將N5單字數據插入到MongoDB資料庫"""
    # 讀取PDF數據
    logger.info(f"開始從 {DATA_FILE_PATH} 讀取數據")
    data = read_pdf_data(DATA_FILE_PATH)

    if not data:
        logger.warning("沒有找到有效的數據")
        return

    # 獲取MongoDB連接
    logger.info("正在連接MongoDB資料庫")
    db_manager = DBManager()
    success_count = 0

    try:
        # 獲取集合並進行數據插入
        collection = db_manager.crud.collection
        if db_manager.db is None or collection is None:
            logger.error("無法連接到MongoDB或collection不存在")
            return

        # 批量檢查已存在的單詞
        existing_words = set()
        all_japanese = [word["japanese"] for word in data]
        for chunk in [
            all_japanese[i : i + 100] for i in range(0, len(all_japanese), 100)
        ]:
            for doc in collection.find({"japanese": {"$in": chunk}}, {"japanese": 1}):
                existing_words.add(doc["japanese"])

        # 處理每個單詞
        for word in data:
            try:
                if word["japanese"] in existing_words:
                    logger.debug(f"單詞已存在，跳過: {word['japanese']}")
                    continue

                # 插入數據
                result = collection.insert_one(word)
                if result.inserted_id:
                    success_count += 1
                    if success_count % 50 == 0:  # 每50個成功插入記錄一次
                        logger.info(f"已成功插入 {success_count} 個單詞")
                else:
                    logger.warning(f"插入失敗: {word['japanese']} - {word['meaning']}")
            except Exception as e:
                logger.error(f"插入數據時發生錯誤: {word['japanese']} - {e}")

    finally:
        # 關閉數據庫連接
        db_manager.close_connection()
        logger.info("已關閉與MongoDB的連接")

    logger.info(f"總共成功插入 {success_count} 筆資料")


if __name__ == "__main__":
    insert_n5_data()
