from sqlalchemy.orm import Session
from app.models.estudante import Estudante
from app.schemas.estudante import EstudanteCreate

class EstudanteRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_estudante(self, estudante_id: int) -> Estudante | None:
        return self.db.query(Estudante).filter(Estudante.id == estudante_id).first()

    def get_estudantes(self, skip: int = 0, limit: int = 10) -> list[Estudante]:
        return self.db.query(Estudante).offset(skip).limit(limit).all()

    def create_estudante(self, estudante: EstudanteCreate) -> Estudante:
        db_estudante = Estudante(**estudante.dict())
        self.db.add(db_estudante)
        self.db.commit()
        self.db.refresh(db_estudante)
        return db_estudante

    def update_estudante(self, estudante_id: int, estudante: EstudanteCreate) -> Estudante | None:
        db_estudante = self.get_estudante(estudante_id)
        if db_estudante:
            for key, value in estudante.dict().items():
                setattr(db_estudante, key, value)
            self.db.commit()
            self.db.refresh(db_estudante)
        return db_estudante

    def delete_estudante(self, estudante_id: int) -> bool:
        db_estudante = self.get_estudante(estudante_id)
        if db_estudante:
            self.db.delete(db_estudante)
            self.db.commit()
            return True
        return False