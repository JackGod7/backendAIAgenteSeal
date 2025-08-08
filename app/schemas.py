from pydantic import BaseModel
from typing import Optional

class QADataModelBase(BaseModel):
    Comentario: Optional[str]
    Respuesta: Optional[str]
    Tema: Optional[str]

class QADataModelCreate(QADataModelBase):
    pass

class QADataModelUpdate(QADataModelBase):
    pass

class QADataModelOut(QADataModelBase):
    ID: int

    class Config:
        from_attributes = True