from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app import crud, schemas

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # frontend Angular
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencia de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/login", response_model=schemas.UserLoginOut)
def login(user_data: schemas.UserLoginBase, db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, user_data.user, user_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    return user

@app.post("/login/change-password")
def change_password(data: schemas.ChangePasswordRequest, db: Session = Depends(get_db)):
    updated_user = crud.change_password(db, data.user, data.old_password, data.new_password)
    if not updated_user:
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    return {"message": "Contraseña cambiada correctamente"}

# Rutas CRUD
@app.get("/items/", response_model=list[schemas.QADataModelOut])
def read_items(db: Session = Depends(get_db)):
    return crud.get_all_entries(db)

@app.get("/items/{item_id}", response_model=schemas.QADataModelOut)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_entry_by_id(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.post("/items/", response_model=schemas.QADataModelOut)
def create_item(item: schemas.QADataModelCreate, db: Session = Depends(get_db)):
    return crud.create_entry(db, item)

@app.put("/items/{item_id}", response_model=schemas.QADataModelOut)
def update_item(item_id: int, item: schemas.QADataModelUpdate, db: Session = Depends(get_db)):
    db_item = crud.update_entry(db, item_id, item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.delete("/items/{item_id}", response_model=schemas.QADataModelOut)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.delete_entry(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item
