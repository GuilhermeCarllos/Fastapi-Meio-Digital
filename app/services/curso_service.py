from sqlalchemy.orm import Session
from app.models.curso import Curso as CursoModel
from app.schemas.curso import CursoCreate, Curso
from app.repositories.curso_repository import CursoRepository

class CursoService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = CursoRepository(db)

    def create_curso(self, curso: CursoCreate) -> Curso:
        db_curso = CursoModel(**curso.dict())
        self.db.add(db_curso)
        self.db.commit()
        self.db.refresh(db_curso)
        return db_curso

    def get_cursos(self) -> list[Curso]:
        return self.repo.get_cursos()

    def get_curso(self, curso_id: int) -> Curso | None:
        return self.repo.get_curso(curso_id)

    def update_curso(self, curso_id: int, curso: CursoCreate) -> Curso | None:
        return self.repo.update_curso(curso_id, curso)

    def delete_curso(self, curso_id: int) -> bool:
        return self.repo.delete_curso(curso_id)