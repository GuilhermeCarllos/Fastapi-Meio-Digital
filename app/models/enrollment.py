from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base

class Enrollment(Base):
    __tablename__ = "enrollments"
    id = Column(Integer, primary_key=True, index=True)
    estudante_id = Column(Integer, ForeignKey("estudantes.id"), nullable=False)
    curso_id = Column(Integer, ForeignKey("cursos.id"), nullable=False)

    # Relacionamentos
    estudante = relationship("Estudante", back_populates="enrollments")
    curso = relationship("Curso", back_populates="enrollments")