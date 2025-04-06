from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.schemas.professor import ProfessorCreate, Professor
from app.repositories.professor_repository import ProfessorRepository
from app.models.professor import Professor as ProfessorModel

class ProfessorService:
    def __init__(self, db: Session):
        self.repo = ProfessorRepository(db)
        self.db = db

    def create_professor(self, professor: ProfessorCreate) -> Professor:
        existing_professor = self.db.query(ProfessorModel).filter(ProfessorModel.email == professor.email).first()
        if existing_professor:
            raise ValueError(f"E-mail {professor.email} já está em uso")
        
        try:
            return self.repo.create_professor(professor)
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Erro ao criar professor: possível duplicação de e-mail")

    def get_professor(self, professor_id: int) -> Professor | None:
        return self.repo.get_professor(professor_id)

    def get_professores(self) -> list[Professor]:
        return self.repo.get_professores()

    def update_professor(self, professor_id: int, professor: ProfessorCreate) -> Professor | None:
        return self.repo.update_professor(professor_id, professor)

    def delete_professor(self, professor_id: int) -> bool:
        return self.repo.delete_professor(professor_id)