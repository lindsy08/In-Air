
from pydantic import BaseModel, Field, ConfigDict, model_validator


class UmbralCrear(BaseModel):
    id_tipo_sensor: int = Field(gt=0)
    id_salon: int = Field(gt=0)
    valor_minimo: float = Field(allow_inf_nan=False)
    valor_maximo: float = Field(allow_inf_nan=False)
    descripcion: str | None = Field(
        default=None,
        max_length=200
    )

    model_config = ConfigDict(str_strip_whitespace=True)

    @model_validator(mode="after")
    def validar_rango(self):
        if self.valor_minimo >= self.valor_maximo:
            raise ValueError(
                "El valor mínimo debe ser menor que el máximo."
            )
        return self


class UmbralActualizar(UmbralCrear):
    pass
