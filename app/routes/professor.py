from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.professor import ProfessorCreate, Professor
from app.services.professor_service import ProfessorService
from app.database.database import get_db
from app.routes.auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/create-json", response_model=Professor)
def create_professor(professor: ProfessorCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Cria um novo professor via JSON."""
    try:
        professor_service = ProfessorService(db)
        return professor_service.create_professor(professor)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/professors", response_model=list[Professor])
def get_professors(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Retorna todos os professores."""
    professor_service = ProfessorService(db)
    return professor_service.get_professores()

@router.get("/professor/{professor_id}", response_model=Professor)
def get_professor(professor_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Retorna um professor pelo ID."""
    professor_service = ProfessorService(db)
    professor = professor_service.get_professor(professor_id)
    if not professor:
        raise HTTPException(status_code=404, detail="Professor não encontrado")
    return professor

@router.put("/professor/{professor_id}", response_model=Professor)
def update_professor(professor_id: int, professor: ProfessorCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Atualiza um professor existente."""
    professor_service = ProfessorService(db)
    updated_professor = professor_service.update_professor(professor_id, professor)
    if not updated_professor:
        raise HTTPException(status_code=404, detail="Professor não encontrado")
    return updated_professor

@router.delete("/professor/{professor_id}")
def delete_professor(professor_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Deleta um professor pelo ID."""
    professor_service = ProfessorService(db)
    if not professor_service.delete_professor(professor_id):
        raise HTTPException(status_code=404, detail="Professor não encontrado")
    return {"message": "Professor deletado com sucesso"}