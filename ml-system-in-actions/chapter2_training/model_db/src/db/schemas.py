import datetime
from typing import Dict, Optional

from pydantic import BaseModel


# 定義一個基本的專案 Schema，繼承自 BaseModel，用於描述專案的共通欄位
class ProjectBase(BaseModel):
    # 表示專案名稱，必須是字串型態，作為專案的主要識別資訊
    project_name: str
    # 描述欄位為可選字串，用來補充說明專案內容，允許傳入 None 表示沒有提供描述
    description: Optional[str]


# 繼承自 ProjectBase，用於新增專案時接收前端傳入的資料
class ProjectCreate(ProjectBase):
    pass


# 在 ProjectBase 的基礎上，增加了資料庫內部產生的額外欄位
class Project(ProjectBase):
    # 代表專案在資料庫中的唯一識別碼，此處設計為整數
    # （注意：若資料庫中實際使用字串，此處可能需對應調整）
    project_id: int
    # 記錄專案建立的日期與時間，使用 datetime 型態，方便後續進行時間相關運算或格式化顯示
    created_datetime: datetime.datetime

    # 啟用 ORM 模式，使 Pydantic 可以直接從 ORM 物件（例如 SQLAlchemy 模型）中讀取屬性，方便資料轉換與序列化
    class Config:
        orm_mode = True


# 定義模型的基本 Schema，描述模型共通欄位
class ModelBase(BaseModel):
    # 表示該模型所屬的專案識別碼，這裡定義為字串，通常與資料庫中專案關聯使用
    project_id: str
    # 模型名稱，必填字串，作為辨識模型的主要資訊
    model_name: str
    # 模型的描述欄位，允許為空，用來記錄模型的補充資訊
    description: Optional[str]


# 繼承自 ModelBase，用於新增模型時接收前端資料
class ModelCreate(ModelBase):
    pass


# 在 ModelBase 的基礎上增加模型在資料庫中獨有的欄位
class Model(ModelBase):
    # 模型在資料庫中的唯一識別碼，設計為整數（若資料庫實際使用字串則需調整）
    model_id: int
    # 記錄模型建立的日期與時間，方便追蹤或顯示建立時間
    created_datetime: datetime.datetime

    # 同樣啟用 ORM 模式，方便將 ORM 模型轉換為 Pydantic 物件
    class Config:
        orm_mode = True


# 定義實驗的基礎 Schema，描述實驗的所有主要欄位
class ExperimentBase(BaseModel):
    # 表示該實驗所屬的模型識別碼，連結實驗與模型
    model_id: str
    # 用來記錄實驗中使用的模型版本號，方便區分不同版本的實驗結果
    model_version_id: str
    # 儲存學習或模型參數，使用字典型態以便存放結構化的參數資料
    parameters: Optional[Dict]
    # 儲存訓練數據的相關資訊（例如檔案路徑或描述），允許為空
    training_dataset: Optional[str]
    # 儲存訓練數據的相關資訊（例如檔案路徑或描述），允許為空
    validation_dataset: Optional[str]
    # 儲存測試數據的相關資訊
    test_dataset: Optional[str]
    # 儲存模型評估結果，使用字典以支援多指標的評估資料
    evaluations: Optional[Dict]
    # 儲存實驗產生的檔案路徑資料，支援多檔案與結構化資料的存放
    artifact_file_paths: Optional[Dict]


# 繼承自 ExperimentBase，用於新增實驗資料時接收前端傳入的資料，無需額外欄位
class ExperimentCreate(ExperimentBase):
    pass


# 定義專門用來更新或處理實驗評估結果的 Schema，只包含 evaluations 欄位
class ExperimentEvaluations(BaseModel):
    # 強制要求評估結果必須是字典型態，用於局部更新操作時清楚限定更新內容
    evaluations: Dict


# 定義專門用來更新實驗中模型檔案路徑的 Schema，僅包含 artifact_file_paths 欄位
class ExperimentArtifactFilePaths(BaseModel):
    # 限定傳入的資料型態為字典，便於局部更新檔案路徑資訊
    artifact_file_paths: Dict


# 在 ExperimentBase 的基礎上，增加了實驗的唯一識別碼與建立時間
class Experiment(ExperimentBase):
    # 表示實驗在資料庫中的唯一識別碼，設計為整數（實際上若資料庫為字串也可做相應調整）
    experiment_id: int
    # 記錄實驗建立時的日期與時間，有助於追蹤與排序實驗紀錄
    created_datetime: datetime.datetime

    # 啟用 ORM 模式，讓 Pydantic 可以直接從 ORM 模型轉換成這些 Schema，簡化資料處理流程
    class Config:
        orm_mode = True
