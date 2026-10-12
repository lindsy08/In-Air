
from pydantic import BaseModel, Field, ConfigDict


class ModuloCrear(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    ruta: str = Field(
        min_length=2,
        max_length=150,
        pattern=r"^/[a-z0-9/_-]+$"
    )
    descripcion: str | None = Field(
        default=None,
        max_length=200
    )

    model_config = ConfigDict(str_strip_whitespace=True)


class ModuloActualizar(ModuloCrear):
    pass
