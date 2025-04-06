from sqlalchemy.orm import Session
from app.models.professor import Professor
from app.schemas.professor import ProfessorCreate

class ProfessorRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_professor(self, professor_id: int) -> Professor | None:
        return self.db.query(Professor).filter(Professor.id == professor_id).first()

    def get_professores(self, skip: int = 0, limit: int = 10) -> list[Professor]:
        return self.db.query(Professor).offset(skip).limit(limit).all()

    def create_professor(self, professor: ProfessorCreate) -> Professor:
        db_professor = Professor(**professor.dict())
        self.db.add(db_professor)
        self.db.commit()
        self.db.refresh(db_professor)
        return db_professor

    def update_professor(self, professor_id: int, professor: ProfessorCreate) -> Professor | None:
        db_professor = self.get_professor(professor_id)
        if db_professor:
            for key, value in professor.dict().items():
                setattr(db_professor, key, value)
            self.db.commit()
            self.db.refresh(db_professor)
        return db_professor

    def delete_professor(self, professor_id: int) -> bool:
        db_professor = self.get_professor(professor_id)
        if db_professor:
            self.db.delete(db_professor)
            self.db.commit()
            return True
        return False