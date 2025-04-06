from sqlalchemy.orm import Session
from app.models.enrollment import Enrollment
from app.schemas.enrollment import EnrollmentCreate

class EnrollmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_enrollment(self, enrollment_id: int) -> Enrollment | None:
        return self.db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()

    def get_enrollments(self, skip: int = 0, limit: int = 10) -> list[Enrollment]:
        return self.db.query(Enrollment).offset(skip).limit(limit).all()

    def create_enrollment(self, enrollment: EnrollmentCreate) -> Enrollment:
        db_enrollment = Enrollment(**enrollment.dict())
        self.db.add(db_enrollment)
        self.db.commit()
        self.db.refresh(db_enrollment)
        return db_enrollment

    def update_enrollment(self, enrollment_id: int, enrollment: EnrollmentCreate) -> Enrollment | None:
        db_enrollment = self.get_enrollment(enrollment_id)
        if db_enrollment:
            for key, value in enrollment.dict().items():
                setattr(db_enrollment, key, value)
            self.db.commit()
            self.db.refresh(db_enrollment)
        return db_enrollment

    def delete_enrollment(self, enrollment_id: int) -> bool:
        db_enrollment = self.get_enrollment(enrollment_id)
        if db_enrollment:
            self.db.delete(db_enrollment)
            self.db.commit()
            return True
        return False