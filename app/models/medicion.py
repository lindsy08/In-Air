
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, ConfigDict


class MedicionCrear(BaseModel):
    id_sensor: int = Field(gt=0)
    id_usuario_registro: int | None = Field(
        default=None,
        gt=0
    )
    valor: float = Field(allow_inf_nan=False)
    fecha_medicion: datetime
    origen: Literal[
        "manual",
        "automatico",
        "simulado"
    ] = "simulado"

    model_config = ConfigDict(str_strip_whitespace=True)


class MedicionActualizar(MedicionCrear):
    pass
