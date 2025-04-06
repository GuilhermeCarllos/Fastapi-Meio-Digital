from pydantic import BaseModel

class ProfessorBase(BaseModel):
    name: str
    email: str

class ProfessorCreate(ProfessorBase):
    pass

class Professor(ProfessorBase):
    id: int

    class Config:
        from_attributes = True  # Corrigido de orm_mode para from_attributes