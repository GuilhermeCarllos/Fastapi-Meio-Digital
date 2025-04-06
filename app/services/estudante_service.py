from sqlalchemy.orm import Session
from fastapi import HTTPException  # Importação adicionada
from app.schemas.estudante import EstudanteCreate, Estudante
from app.models.estudante import Estudante as EstudanteModel

class EstudanteService:
    def __init__(self, db: Session):
        self.db = db

    def create_estudante(self, estudante: EstudanteCreate) -> Estudante:
        db_estudante = EstudanteModel(**estudante.dict())
        self.db.add(db_estudante)
        self.db.commit()
        self.db.refresh(db_estudante)
        return db_estudante

    def get_estudantes(self) -> list[Estudante]:
        return self.db.query(EstudanteModel).all()

    def update_estudante(self, estudante_id: int, estudante: EstudanteCreate) -> Estudante:
        db_estudante = self.db.query(EstudanteModel).filter(EstudanteModel.id == estudante_id).first()
        if not db_estudante:
            raise HTTPException(status_code=404, detail="Estudante não encontrado")
        for key, value in estudante.dict().items():
            setattr(db_estudante, key, value)
        self.db.commit()
        self.db.refresh(db_estudante)
        return db_estudante

    def delete_estudante(self, estudante_id: int) -> None:
        db_estudante = self.db.query(EstudanteModel).filter(EstudanteModel.id == estudante_id).first()
        if not db_estudante:
            raise HTTPException(status_code=404, detail="Estudante não encontrado")
        self.db.delete(db_estudante)
        self.db.commit()