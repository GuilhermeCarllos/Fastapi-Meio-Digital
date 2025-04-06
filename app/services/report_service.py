from sqlalchemy.orm import Session
from app.models.professor import Professor
from app.models.curso import Curso
from app.models.enrollment import Enrollment

class ReportService:
    def __init__(self, db: Session):
        self.db = db

    def get_professores(self):
        return self.db.query(Professor).all()

    def get_cursos(self):
        return self.db.query(Curso).all()

    def get_all_enrollments(self):
        return self.db.query(Enrollment).all()