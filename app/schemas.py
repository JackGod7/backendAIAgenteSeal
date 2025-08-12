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

class ChangePasswordRequest(BaseModel):
    user: str
    old_password: str
    new_password: str

class UserLoginBase(BaseModel):
    user: str
    password: str

class UserLoginCreate(UserLoginBase):
    pass

class UserLoginOut(BaseModel):
    id: int
    user: str

    class Config:
        from_attributes = True