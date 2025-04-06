from pydantic import BaseModel

class CursoBase(BaseModel):
    name: str
    description: str  # Incluído

class CursoCreate(CursoBase):
    pass

class Curso(CursoBase):
    id: int

    class Config:
        from_attributes = True