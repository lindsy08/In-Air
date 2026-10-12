
from pydantic import BaseModel, Field


class RolCrear(BaseModel):
    nombre: str = Field(min_length=2, max_length=50)
    descripcion: str | None = None


class RolActualizar(BaseModel):
    nombre: str = Field(min_length=2, max_length=50)
    descripcion: str | None = None
