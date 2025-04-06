from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.schemas.curso import CursoCreate, Curso
from app.services.curso_service import CursoService
from app.database.database import get_db
from app.routes.auth import get_current_user
from app.models.user import User
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.post("/create-json", response_model=Curso)
def create_curso_json(curso: CursoCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = CursoService(db)
    return service.create_curso(curso)

@router.get("/", response_model=list[Curso])  # Alterado de "/cursos" para "/"
def get_cursos(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = CursoService(db)
    return service.get_cursos()

@router.get("/{curso_id}", response_model=Curso)
def get_curso(curso_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = CursoService(db)
    curso = service.get_curso(curso_id)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    return curso

@router.put("/{curso_id}", response_model=Curso)
def update_curso(curso_id: int, curso: CursoCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = CursoService(db)
    updated_curso = service.update_curso(curso_id, curso)
    if not updated_curso:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    return updated_curso

@router.delete("/{curso_id}")
def delete_curso(curso_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = CursoService(db)
    if not service.delete_curso(curso_id):
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    return {"message": "Curso deletado com sucesso"}