from sqlalchemy.orm import Session
from app.models.enrollment import Enrollment as EnrollmentModel
from app.models.estudante import Estudante
from app.models.curso import Curso
from app.schemas.enrollment import EnrollmentCreate, Enrollment
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnrollmentService:
    def __init__(self, db: Session):
        self.db = db

    def create_enrollment(self, enrollment: EnrollmentCreate) -> Enrollment:
        # Verifica se o estudante existe
        estudante = self.db.query(Estudante).filter(Estudante.id == enrollment.estudante_id).first()
        if not estudante:
            logger.error(f"Estudante com id {enrollment.estudante_id} não encontrado")
            raise ValueError(f"Estudante com id {enrollment.estudante_id} não encontrado")

        # Verifica se o curso existe
        curso = self.db.query(Curso).filter(Curso.id == enrollment.curso_id).first()
        if not curso:
            logger.error(f"Curso com id {enrollment.curso_id} não encontrado")
            raise ValueError(f"Curso com id {enrollment.curso_id} não encontrado")

        # Verifica se a matrícula já existe
        existing_enrollment = self.db.query(EnrollmentModel).filter(
            EnrollmentModel.estudante_id == enrollment.estudante_id,
            EnrollmentModel.curso_id == enrollment.curso_id
        ).first()
        if existing_enrollment:
            logger.warning(f"Matrícula já existe para estudante {enrollment.estudante_id} e curso {enrollment.curso_id}")
            raise ValueError("O estudante já está matriculado neste curso")

        # Log antes da inserção
        logger.info(f"Tentando criar matrícula: estudante_id={enrollment.estudante_id}, curso_id={enrollment.curso_id}")

        # Criar a matrícula
        db_enrollment = EnrollmentModel(estudante_id=enrollment.estudante_id, curso_id=enrollment.curso_id)
        self.db.add(db_enrollment)
        self.db.commit()
        self.db.refresh(db_enrollment)
        logger.info(f"Matrícula criada com sucesso: ID {db_enrollment.id}")
        return Enrollment.model_validate(db_enrollment)  # Pydantic v2

    def get_enrollments(self) -> list[Enrollment]:
        enrollments = self.db.query(EnrollmentModel).all()
        return [Enrollment.model_validate(enrollment) for enrollment in enrollments]