
from pydantic import BaseModel, Field, ConfigDict


class SalonCrear(BaseModel):
    id_edificio: int = Field(gt=0)
    codigo: str = Field(min_length=1, max_length=50)
    piso: int = Field(ge=0)
    capacidad: int = Field(gt=0)
    area_m2: float = Field(gt=0)
    altura_m: float = Field(gt=0)

    model_config = ConfigDict(str_strip_whitespace=True)


class SalonActualizar(SalonCrear):
    pass
