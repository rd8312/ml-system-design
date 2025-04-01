import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.configurations import DBConfigurations

# create_engine 用來建立資料庫引擎（Engine）
# 它是 SQLAlchemy 與資料庫之間的橋樑，負責管理資料庫連線池及發送 SQL 語句
engine = create_engine(
    # 匯入自訂的資料庫設定，此模組通常包含資料庫連線字串（URL）等設定參數
    # 使程式碼與環境設定分離、便於管理與修改
    # 使用設定檔中定義的資料庫連線 URL
    # 這樣可以依據不同環境（開發、測試、生產）靈活調整連線資訊
    DBConfigurations.sql_alchemy_database_url,
    encoding="utf-8",
    # 設定連線池中每個連線的回收時間（單位：秒）
    # 這可以避免資料庫連線因為閒置時間過長而被資料庫伺服器中斷
    # 3600 秒代表一小時回收一次
    pool_recycle=3600,
    # 關閉 SQLAlchemy 的 SQL 語句輸出（debug 訊息）
    # 在開發階段可以設為 True 以方便除錯，但正式環境通常關閉以提高效能與安全性
    echo=False,
)

# sessionmaker 是一個 Session 工廠，用來產生操作資料庫的 Session 物件
# 這些 Session 負責追蹤 ORM 物件的狀態與管理事務
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# declarative_base 用來建立 ORM 模型的基底類別
# 所有後續定義的資料庫模型都會繼承這個類別，方便 SQLAlchemy 自動建立對應的資料表結構
Base = declarative_base()


# 定義一個生成器函式，用於取得資料庫 Session
# 常見於依賴注入（例如 FastAPI 中的 Depends）
def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.rollback()
        raise
    finally:
        db.close()


# 使用 contextlib 中的 @contextmanager 裝飾器，將一個生成器函式轉換為一個上下文管理器
# 這樣就可以用 with 語法來管理 Session 的生命週期
@contextmanager
# 定義另一個取得 Session 的方法，與 get_db() 功能類似
# 但透過上下文管理器的方式使用，使得資源釋放更加自動化與直觀
def get_context_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.rollback()
        raise
    finally:
        db.close()
