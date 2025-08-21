from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional

from . import models
from . import schemas

# -------------------- CRUD QADataModel --------------------

def get_all_entries(db: Session):
    return db.query(models.QADataModel).all()

def get_paginated_entries(
    db: Session,
    page: int,
    page_size: int,
    search: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_order: str = 'asc'
):
    query = db.query(models.QADataModel)

    if search:
        search_term = f"%{search}%"
        
        filter_conditions = [
            models.QADataModel.Comentario.ilike(search_term),
            models.QADataModel.Respuesta.ilike(search_term),
            models.QADataModel.Tema.ilike(search_term),
        ]

        query = query.filter(or_(*filter_conditions))


    total_items = query.count()

    if sort_by:
        column_to_sort = getattr(models.QADataModel, sort_by, None)
        if column_to_sort:
            if sort_order == 'desc':
                query = query.order_by(column_to_sort.desc())
            else:
                query = query.order_by(column_to_sort.asc())
    else:
        query = query.order_by(models.QADataModel.ID)
    
    offset = (page - 1) * page_size
    items = query.offset(offset).limit(page_size).all()
    
    return items, total_items

def get_entry_by_id(db: Session, entry_id: int):
    return db.query(models.QADataModel).filter(models.QADataModel.ID == entry_id).first()

def create_entry(db: Session, entry: schemas.QADataModelCreate):
    db_entry = models.QADataModel(**entry.dict())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

def update_entry(db: Session, entry_id: int, entry: schemas.QADataModelUpdate):
    db_entry = db.query(models.QADataModel).filter(models.QADataModel.ID == entry_id).first()
    if db_entry:
        for field, value in entry.dict(exclude_unset=True).items():
            setattr(db_entry, field, value)
        db.commit()
        db.refresh(db_entry)
    return db_entry

def delete_entry(db: Session, entry_id: int):
    db_entry = db.query(models.QADataModel).filter(models.QADataModel.ID == entry_id).first()
    if db_entry:
        db.delete(db_entry)
        db.commit()
    return db_entry

# -------------------- Login --------------------
def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.UserLogin).filter(models.UserLogin.user == username).first()
    if user and user.password == password: 
        return user
    return None

def change_password(db: Session, username: str, old_password: str, new_password: str):
    user = authenticate_user(db, username, old_password)
    if not user:
        return None
    
    user.password = new_password
    db.commit()
    db.refresh(user)
    return user