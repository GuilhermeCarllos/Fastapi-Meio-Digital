from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.database import Base

class Estudante(Base):
    __tablename__ = "estudantes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    # Relacionamento com matrículas
    enrollments = relationship("Enrollment", back_populates="estudante")