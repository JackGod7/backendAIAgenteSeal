from sqlalchemy import Column, Integer, String
from app.database import Base

class QADataModel(Base):
    __tablename__ = "qa_data_model"

    ID = Column(Integer, primary_key=True, index=True)
    Comentario = Column(String, nullable=True)
    Respuesta = Column(String, nullable=True)
    Tema = Column(String(255), nullable=True)
