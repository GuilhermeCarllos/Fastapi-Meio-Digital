from pydantic import BaseModel

class EnrollmentCreate(BaseModel):
    estudante_id: int
    curso_id: int

class Estudante(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True  # Pydantic v2

class Curso(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True  # Pydantic v2

class Enrollment(BaseModel):
    id: int
    estudante_id: int
    curso_id: int
    estudante: Estudante  # Modelo aninhado em vez de dict
    curso: Curso          # Modelo aninhado em vez de dict

    class Config:
        from_attributes = True  # Pydantic v2