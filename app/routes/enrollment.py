from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.enrollment import EnrollmentCreate, Enrollment
from app.services.enrollment_service import EnrollmentService
from app.database.database import get_db
from app.routes.auth import get_current_user
from app.models.user import User

router = APIRouter(tags=["Enrollments"])

@router.post("/", response_model=Enrollment)
def create_enrollment(enrollment: EnrollmentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = EnrollmentService(db)
    try:
        return service.create_enrollment(enrollment)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))