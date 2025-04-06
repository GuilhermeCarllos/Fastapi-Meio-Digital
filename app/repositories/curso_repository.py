from sqlalchemy.orm import Session
from app.models.curso import Curso as CursoModel
from app.schemas.curso import CursoCreate, Curso

class CursoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_curso(self, curso: CursoCreate) -> Curso:
        db_curso = CursoModel(**curso.dict())
        self.db.add(db_curso)
        self.db.commit()
        self.db.refresh(db_curso)
        return db_curso

    def get_curso(self, curso_id: int) -> Curso | None:
        return self.db.query(CursoModel).filter(CursoModel.id == curso_id).first()

    def get_cursos(self, skip: int = 0, limit: int = 10) -> list[Curso]:
        return self.db.query(CursoModel).offset(skip).limit(limit).all()

    def update_curso(self, curso_id: int, curso: CursoCreate) -> Curso | None:
        db_curso = self.get_curso(curso_id)
        if db_curso:
            for key, value in curso.dict().items():
                setattr(db_curso, key, value)
            self.db.commit()
            self.db.refresh(db_curso)
        return db_curso

    def delete_curso(self, curso_id: int) -> bool:
        db_curso = self.get_curso(curso_id)
        if db_curso:
            self.db.delete(db_curso)
            self.db.commit()
            return True
        return False