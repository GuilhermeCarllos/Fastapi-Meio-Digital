from pydantic import BaseModel

class EstudanteBase(BaseModel):
    name: str

class EstudanteCreate(EstudanteBase):
    pass

class Estudante(EstudanteBase):
    id: int

    class Config:
        from_attributes = True