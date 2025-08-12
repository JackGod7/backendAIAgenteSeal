from sqlalchemy import Column, Integer, String
from app.database import Base

class QADataModel(Base):
    __tablename__ = "qa_data_model"

    ID = Column(Integer, primary_key=True, index=True)
    Comentario = Column(String, nullable=True)
    Respuesta = Column(String, nullable=True)
    Tema = Column(String(255), nullable=True)



class UserLogin(Base):
    __tablename__ = "user_agent_ai"  

    id = Column(Integer, primary_key=True, index=True)
    user = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)