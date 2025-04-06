from fastapi import FastAPI, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.routes import curso, estudante, professor, enrollment, report, auth
from app.database.database import Base, engine, get_db
from app.routes.auth import get_current_user
from app.models.user import User
from fastapi.security import OAuth2PasswordBearer
from typing import Optional

app = FastAPI(title="Meio Digital")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

print("Iniciando o servidor FastAPI - Meio Digital")

Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/api/auth")
app.include_router(curso.router, prefix="/api/curso")
app.include_router(estudante.router, prefix="/api/estudante", tags=["Estudante"])
app.include_router(professor.router, prefix="/api/professor")
app.include_router(enrollment.router, prefix="/api/enrollments", tags=["Enrollments"])
app.include_router(report.router, prefix="/api/report")

try:
    Base.metadata.create_all(bind=engine)
    print("Tabelas do banco de dados criadas com sucesso")
except Exception as e:
    print(f"Erro ao criar as tabelas do banco de dados: {e}")
    raise

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)

@app.get("/")
async def read_root(request: Request, token: Optional[str] = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    if token:
        try:
            current_user = get_current_user(token, db)
            if current_user:
                return RedirectResponse(url="/api/report/report")
        except Exception:
            pass
    return RedirectResponse(url="/api/auth/login")

@app.get("/curso")
def curso_page(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    print("Acessando a rota /curso")
    from app.services.curso_service import CursoService
    service = CursoService(db)
    cursos = service.get_cursos()
    return templates.TemplateResponse("curso.html", {"request": request, "cursos": cursos})

@app.get("/estudante")
def estudante_page(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    print("Acessando a rota /estudante")
    from app.services.estudante_service import EstudanteService
    service = EstudanteService(db)
    estudantes = service.get_estudantes()
    formatted_estudantes = [{"id": s.id, "name": s.name} for s in estudantes]  # Removido "email"
    return templates.TemplateResponse("estudante.html", {"request": request, "estudantes": formatted_estudantes})

@app.get("/professor")
def professor_page(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    print("Acessando a rota /professor")
    from app.services.professor_service import ProfessorService
    service = ProfessorService(db)
    professores = service.get_professores()
    return templates.TemplateResponse("professor.html", {"request": request, "professores": professores})

@app.get("/enrollments")
def enrollments_page(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    print("Acessando a rota /enrollments")
    from app.services.enrollment_service import EnrollmentService
    service = EnrollmentService(db)
    enrollments = service.get_enrollments()
    return templates.TemplateResponse("enrollments.html", {"request": request, "enrollments": enrollments})