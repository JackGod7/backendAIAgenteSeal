from sqlalchemy.orm import Session
from app.models import QADataModel, UserLogin
from app.schemas import QADataModelCreate, QADataModelUpdate

# -------------------- CRUD QADataModel --------------------
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


# -------------------- Login --------------------
def authenticate_user(db: Session, username: str, password: str):
    user = db.query(UserLogin).filter(UserLogin.user == username).first()
    if user and user.password == password: 
        return user
    return None

def change_password(db: Session, username: str, old_password: str, new_password: str):
    user = authenticate_user(db, username, old_password)
    if not user:
        return None  # Usuario o contraseña incorrectos
    
    user.password = new_password  # Aquí deberías usar hashing si fuera productivo
    db.commit()
    db.refresh(user)
    return user