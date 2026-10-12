
from datetime import date
from pydantic import BaseModel, Field, ConfigDict


class DispositivoCrear(BaseModel):
    id_salon: int = Field(gt=0)
    codigo: str = Field(min_length=2, max_length=50)
    modelo: str | None = Field(default=None, max_length=100)
    es_virtual: bool = True
    fecha_instalacion: date | None = None

    model_config = ConfigDict(str_strip_whitespace=True)


class DispositivoActualizar(DispositivoCrear):
    pass
