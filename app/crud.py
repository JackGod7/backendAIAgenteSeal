from sqlalchemy.orm import Session
from app.models import QADataModel
from app.schemas import QADataModelCreate, QADataModelUpdate

def get_all_entries(db: Session):
    return db.query(QADataModel).all()

def get_entry_by_id(db: Session, entry_id: int):
    return db.query(QADataModel).filter(QADataModel.ID == entry_id).first()

def create_entry(db: Session, entry: QADataModelCreate):
    db_entry = QADataModel(**entry.dict())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

def update_entry(db: Session, entry_id: int, entry: QADataModelUpdate):
    db_entry = db.query(QADataModel).filter(QADataModel.ID == entry_id).first()
    if db_entry:
        for field, value in entry.dict(exclude_unset=True).items():
            setattr(db_entry, field, value)
        db.commit()
        db.refresh(db_entry)
    return db_entry

def delete_entry(db: Session, entry_id: int):
    db_entry = db.query(QADataModel).filter(QADataModel.ID == entry_id).first()
    if db_entry:
        db.delete(db_entry)
        db.commit()
    return db_entry
