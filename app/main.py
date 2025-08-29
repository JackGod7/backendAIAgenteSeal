from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional  

from app.database import SessionLocal, engine, Base
from app import crud, schemas

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:4200",          # Origen para pruebas en la misma VM
    "http://192.168.52.60:4200",     # Origen para el acceso desde tu PC
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# --- RUTA MODIFICADA ---
@app.get("/items/", response_model=schemas.PaginatedQAData)
def read_items_paginated(
    db: Session = Depends(get_db),
    page: int = Query(1, gt=0, description="Número de página"),
    page_size: int = Query(10, gt=0, le=100, description="Items por página"),
    search: Optional[str] = Query(None, description="Término de búsqueda general"),
    sort_by: Optional[str] = Query(None, description="Campo por el cual ordenar (ej: ID, Tema)"),
    sort_order: str = Query('asc', description="Orden ('asc' o 'desc')")
):
    items_from_db, total_items = crud.get_paginated_entries(
        db, 
        page=page, 
        page_size=page_size, 
        search=search, 
        sort_by=sort_by, 
        sort_order=sort_order
    )

    start_index = (page - 1) * page_size
    for i, item in enumerate(items_from_db):
        item.NroItem = start_index + i + 1
    
    total_pages = (total_items + page_size - 1) // page_size

    return {
        "total_items": total_items,
        "total_pages": total_pages,
        "current_page": page,
        "items": items_from_db
    }

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