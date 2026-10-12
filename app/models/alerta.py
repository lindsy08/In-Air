
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, ConfigDict


class AlertaCrear(BaseModel):
    id_medicion: int = Field(gt=0)
    id_umbral: int = Field(gt=0)
    nivel: Literal[
        "informativa",
        "advertencia",
        "critica"
    ]
    mensaje: str = Field(min_length=3, max_length=500)
    fecha_alerta: datetime | None = None
    atendida: bool = False

    model_config = ConfigDict(str_strip_whitespace=True)


class AlertaActualizar(AlertaCrear):
    pass
