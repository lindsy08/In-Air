
from pydantic import BaseModel, Field, ConfigDict


class EdificioCrear(BaseModel):
    id_entidad: int = Field(gt=0)
    nombre: str = Field(min_length=2, max_length=100)
    codigo: str = Field(min_length=1, max_length=50)
    numero_pisos: int = Field(gt=0)

    model_config = ConfigDict(str_strip_whitespace=True)


class EdificioActualizar(EdificioCrear):
    pass
