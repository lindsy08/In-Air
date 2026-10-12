
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, ConfigDict


class AccionVentilacionCrear(BaseModel):
    id_salon: int = Field(gt=0)
    id_alerta: int | None = Field(default=None, gt=0)
    codigo: str = Field(min_length=2, max_length=50)
    tipo_accion: str = Field(min_length=3, max_length=100)
    modo: Literal[
        "manual",
        "automatico",
        "simulado"
    ] = "simulado"
    fecha_accion: datetime | None = None
    observacion: str | None = Field(
        default=None,
        max_length=500
    )

    model_config = ConfigDict(str_strip_whitespace=True)


class AccionVentilacionActualizar(AccionVentilacionCrear):
    pass
