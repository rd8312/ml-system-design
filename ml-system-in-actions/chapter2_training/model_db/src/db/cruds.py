import uuid
from typing import Dict, List, Optional

from sqlalchemy.orm import Session
# 引入定義好的資料庫模型（models）以及對應的資料結構（schemas），通常後者用於資料驗證與序列化
from src.db import models, schemas


# 查詢所有專案
def select_project_all(db: Session) -> List[schemas.Project]:
    # 對資料庫中的 Project 表發出查詢，並取得所有記錄
    # 提供快速獲取所有專案資料的接口，方便管理或顯示全部專案列表
    return db.query(models.Project).all()


# 依據專案 ID 查詢
def select_project_by_id(
    db: Session,
    project_id: str,
) -> schemas.Project:
    return db.query(models.Project).filter(models.Project.project_id == project_id).first()


# 依據專案名稱查詢
def select_project_by_name(
    db: Session,
    project_name: str,
) -> schemas.Project:
    return db.query(models.Project).filter(models.Project.project_name == project_name).first()


# 新增專案
def add_project(
    db: Session,
    project_name: str,
    description: Optional[str] = None,
    commit: bool = True,
) -> schemas.Project:
    exists = select_project_by_name(
        db=db,
        project_name=project_name,
    )
    if exists:
        return exists
    else:
        project_id = str(uuid.uuid4())[:6]
        data = models.Project(
            project_id=project_id,
            project_name=project_name,
            description=description,
        )
        db.add(data)
        if commit:
            db.commit()
            db.refresh(data)
        return data


# 查詢所有模型
def select_model_all(db: Session) -> List[schemas.Model]:
    # 直接查詢 Model 表的所有記錄
    # 設計理念：方便獲取所有模型資料以供管理或顯示
    return db.query(models.Model).all()


# 依據模型 ID 查詢
def select_model_by_id(
    db: Session,
    model_id: str,
) -> schemas.Model:
    # 利用模型的唯一 ID 來查詢特定模型，返回第一筆匹配資料
    # 設計理念：主鍵查詢能快速定位唯一記錄
    return db.query(models.Model).filter(models.Model.model_id == model_id).first()


# 依據專案 ID 查詢模型
def select_model_by_project_id(
    db: Session,
    project_id: str,
) -> List[schemas.Model]:
    # 根據 project_id 過濾模型，返回屬於特定專案的所有模型
    # 設計理念：支援依照專案篩選模型，便於在專案內部管理各模型
    return db.query(models.Model).filter(models.Model.project_id == project_id).all()


# 依據專案名稱查詢模型
def select_model_by_project_name(
    db: Session,
    project_name: str,
) -> List[schemas.Model]:
    # 先根據專案名稱查詢專案
    project = select_project_by_name(
        db=db,
        project_name=project_name,
    )
    # 再根據該專案的 project_id 查詢模型回傳該專案下所有模型
    return db.query(models.Model).filter(models.Model.project_id == project.project_id).all()


# 依據模型名稱查詢
def select_model_by_name(
    db: Session,
    model_name: str,
) -> List[schemas.Model]:
    # 直接根據模型名稱過濾查詢，返回所有匹配的模型
    return db.query(models.Model).filter(models.Model.model_name == model_name).all()


# 新增模型
def add_model(
    db: Session,
    project_id: str,
    model_name: str,
    description: Optional[str] = None,
    commit: bool = True,
) -> schemas.Model:
    models_in_project = select_model_by_project_id(
        db=db,
        project_id=project_id,
    )
    for model in models_in_project:
        if model.model_name == model_name:
            return model
    model_id = str(uuid.uuid4())[:6]
    data = models.Model(
        model_id=model_id,
        project_id=project_id,
        model_name=model_name,
        description=description,
    )
    db.add(data)
    if commit:
        db.commit()
        db.refresh(data)
    return data


# 查詢所有實驗
def select_experiment_all(db: Session) -> List[schemas.Experiment]:
    return db.query(models.Experiment).all()

# 查詢所有實驗
def select_experiment_by_id(
    db: Session,
    experiment_id: str,
) -> schemas.Experiment:
    return db.query(models.Experiment).filter(models.Experiment.experiment_id == experiment_id).first()


# 依據模型實驗版本 ID 查詢
def select_experiment_by_model_version_id(
    db: Session,
    model_version_id: str,
) -> schemas.Experiment:
    return db.query(models.Experiment).filter(models.Experiment.model_version_id == model_version_id).first()


# 依據模型 ID 查詢實驗
def select_experiment_by_model_id(
    db: Session,
    model_id: str,
) -> List[schemas.Experiment]:
    return db.query(models.Experiment).filter(models.Experiment.model_id == model_id).all()


# 依據專案 ID 查詢實驗
def select_experiment_by_project_id(
    db: Session,
    project_id: str,
) -> List[schemas.Experiment]:
    return (
        db.query(models.Experiment, models.Model)
        .filter(models.Model.project_id == project_id)
        .filter(models.Experiment.model_id == models.Model.model_id)
        .all()
    )


# 新增實驗
def add_experiment(
    db: Session,
    model_version_id: str,
    model_id: str,
    parameters: Optional[Dict] = None,
    training_dataset: Optional[str] = None,
    validation_dataset: Optional[str] = None,
    test_dataset: Optional[str] = None,
    evaluations: Optional[Dict] = None,
    artifact_file_paths: Optional[Dict] = None,
    commit: bool = True,
) -> schemas.Experiment:
    experiment_id = str(uuid.uuid4())[:6]
    data = models.Experiment(
        experiment_id=experiment_id,
        model_version_id=model_version_id,
        model_id=model_id,
        parameters=parameters,
        training_dataset=training_dataset,
        validation_dataset=validation_dataset,
        test_dataset=test_dataset,
        evaluations=evaluations,
        artifact_file_paths=artifact_file_paths,
    )
    db.add(data)
    if commit:
        db.commit()
        db.refresh(data)
    return data


# 更新實驗的評估結果
def update_experiment_evaluation(
    db: Session,
    experiment_id: str,
    evaluations: Dict,
) -> schemas.Experiment:
    data = select_experiment_by_id(
        db=db,
        experiment_id=experiment_id,
    )
    if data.evaluations is None:
        data.evaluations = evaluations
    else:
        for k, v in evaluations.items():
            data.evaluations[k] = v
    db.commit()
    db.refresh(data)
    return data


#更新實驗的模型檔案路徑
def update_experiment_artifact_file_paths(
    db: Session,
    experiment_id: str,
    artifact_file_paths: Dict,
) -> schemas.Experiment:
    data = select_experiment_by_id(
        db=db,
        experiment_id=experiment_id,
    )
    if data.artifact_file_paths is None:
        data.artifact_file_paths = artifact_file_paths
    else:
        for k, v in artifact_file_paths.items():
            data.artifact_file_paths[k] = v
    db.commit()
    db.refresh(data)
    return data
