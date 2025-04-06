from sqlalchemy import Column, Integer, String
from app.database.database import Base

class Professor(Base):
    __tablename__ = "professores"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, nullable=False)