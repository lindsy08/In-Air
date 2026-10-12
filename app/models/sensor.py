
from pydantic import BaseModel, Field, ConfigDict


class SensorCrear(BaseModel):
    id_dispositivo: int = Field(gt=0)
    id_tipo_sensor: int = Field(gt=0)
    codigo: str = Field(min_length=2, max_length=50)
    modelo: str | None = Field(default=None, max_length=100)

    model_config = ConfigDict(str_strip_whitespace=True)


class SensorActualizar(SensorCrear):
    pass
