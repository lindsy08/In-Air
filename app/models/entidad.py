
from pydantic import BaseModel, Field, ConfigDict


class EntidadCrear(BaseModel):
    nombre: str = Field(min_length=2, max_length=150)
    codigo: str = Field(min_length=2, max_length=50)
    tipo_entidad: str = Field(min_length=2, max_length=80)
    direccion: str | None = Field(default=None, max_length=200)
    correo_contacto: str | None = Field(default=None, max_length=150)

    model_config = ConfigDict(str_strip_whitespace=True)


class EntidadActualizar(EntidadCrear):
    pass
