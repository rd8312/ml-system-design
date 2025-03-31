from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.types import JSON
from src.db.database import Base


# PROJECTS 表單
# 定義一個專案模型，代表一個資料庫中的「專案」實體
class Project(Base):
    # 定義一個專案模型，代表一個資料庫中的「專案」實體
    __tablename__ = "projects"

    project_id = Column(
        String(255),
        primary_key=True,
        comment="主鍵",
    )
    project_name = Column(
        String(255),
        nullable=False, # 此欄位不允許為空，保證每個專案都必須有名稱
        unique=True, # 保證專案名稱在資料庫中唯一，避免重複
        comment="專案名稱",
    )
    description = Column(
        Text, # 儲存專案的描述資訊，使用 Text 型態以應對長篇文字說明
        nullable=True,
        comment="説明",
    )
    created_datetime = Column(
        # 記錄專案建立的日期與時間，型態為 DateTime 且支援時區
        DateTime(timezone=True),
        # 在資料庫端預設值為當前時間，確保每筆資料在建立時自動獲得建立時間
        server_default=current_timestamp(),
        nullable=False, # 此欄位必須有值，不能為空
    )


# MODELS 表單
# 定義一個模型（Model）實體，通常代表專案中所訓練的機器學習模型
class Model(Base):
    # 指定資料表名稱為 models
    __tablename__ = "models"

    model_id = Column(
        String(255),
        primary_key=True,
        comment="主鍵",
    )
    # 這是一個外部鍵，指向 projects 表中的 project_id 欄位，用以建立模型與專案之間的關聯關係
    project_id = Column(
        String(255),
        ForeignKey("projects.project_id"),
        nullable=False, # 確保每個模型都必須關聯到一個專案
        comment="外部鍵",
    )
    model_name = Column(
        String(255),
        nullable=False,
        comment="模型名稱",
    )
    description = Column(
        Text,
        nullable=True,
        comment="説明",
    )
    created_datetime = Column(
        DateTime(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
    )


# EXPERTIMENTS 表單
# 定義實驗（Experiment）模型，通常用來儲存不同版本或參數設定下的模型實驗結果
class Experiment(Base):
    __tablename__ = "experiments"

    # 實驗的唯一識別碼
    experiment_id = Column(
        String(255),
        primary_key=True,
        comment="主鍵",
    )
    # 用來關聯到所屬的模型。這個欄位是外鍵，指向 models 表中的 model_id 欄位
    model_id = Column(
        String(255),
        ForeignKey("models.model_id"),
        nullable=False,
        comment="外部鍵",
    )
    # 記錄模型在實驗中的版本識別（可能代表不同參數、結構等變動）
    model_version_id = Column(
        String(255),
        nullable=False,
        comment="模型的實驗版本 ID",
    )
    # 儲存模型訓練時使用的超參數或其他設定，採用 JSON 格式存放
    parameters = Column(
        JSON,
        nullable=True,
        comment="學習參數",
    )
    # 儲存訓練資料的相關描述或路徑（以文字型態保存）
    training_dataset = Column(
        Text,
        nullable=True,
        comment="學習資料",
    )
    # 儲存驗證（evaluation/validation）資料資訊，同樣使用 Text 型態
    validation_dataset = Column(
        Text,
        nullable=True,
        comment="評估資料",
    )
    # 儲存測試資料相關資訊，型態為 Text
    test_dataset = Column(
        Text,
        nullable=True,
        comment="測試資料",
    )
    # 用於儲存模型在實驗中的評估結果，使用 JSON 格式存放，便於存放結構化數據（例如各種評分、指標）
    evaluations = Column(
        JSON,
        nullable=True,
        comment="評估結果",
    )
    # 儲存實驗產生的檔案路徑（例如模型檔、權重檔等），以 JSON 格式儲存
    artifact_file_paths = Column(
        JSON,
        nullable=True,
        comment="模型檔案的路徑",
    )
    created_datetime = Column(
        DateTime(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
    )
