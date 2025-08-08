from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app import crud, schemas

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
