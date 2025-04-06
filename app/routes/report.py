from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.routes.auth import get_current_user
from app.models.user import User
from app.services.report_service import ReportService

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/report", tags=["Report"])
def report_page(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = ReportService(db)
    professores = service.get_professores()
    cursos = service.get_cursos()
    enrollments = service.get_all_enrollments()
    print(f"Relatório: {len(professores)} professores, {len(cursos)} cursos, {len(enrollments)} matrículas")  # Log para depuração
    return templates.TemplateResponse(
        "report.html",
        {
            "request": request,
            "professores": professores,
            "cursos": cursos,
            "enrollments": enrollments
        }
    )