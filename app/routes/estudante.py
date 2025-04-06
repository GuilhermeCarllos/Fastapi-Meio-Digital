from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.estudante import EstudanteCreate, Estudante
from app.services.estudante_service import EstudanteService
from app.database.database import get_db
from app.routes.auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=Estudante)
def create_estudante(estudante: EstudanteCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = EstudanteService(db)
    return service.create_estudante(estudante)

@router.get("/", response_model=list[Estudante])
def get_estudantes(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = EstudanteService(db)
    return service.get_estudantes()

@router.put("/{estudante_id}", response_model=Estudante)
def update_estudante(estudante_id: int, estudante: EstudanteCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = EstudanteService(db)
    return service.update_estudante(estudante_id, estudante)

@router.delete("/{estudante_id}")
def delete_estudante(estudante_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = EstudanteService(db)
    service.delete_estudante(estudante_id)
    return {"message": "Estudante excluído com sucesso"}