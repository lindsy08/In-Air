
from pydantic import BaseModel, Field, ConfigDict


class TipoSensorCrear(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    unidad_medida: str = Field(min_length=1, max_length=30)
    descripcion: str | None = Field(
        default=None,
        max_length=200
    )

    model_config = ConfigDict(str_strip_whitespace=True)


class TipoSensorActualizar(TipoSensorCrear):
    pass
