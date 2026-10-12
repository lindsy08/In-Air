
from pydantic import BaseModel, Field, EmailStr, ConfigDict


class UsuarioCrear(BaseModel):
    id_rol: int = Field(gt=0)
    nombre: str = Field(min_length=2, max_length=100)
    apellido: str = Field(min_length=2, max_length=100)
    correo: EmailStr
    password: str = Field(min_length=8, max_length=128)

    model_config = ConfigDict(str_strip_whitespace=True)


class UsuarioActualizar(BaseModel):
    id_rol: int = Field(gt=0)
    nombre: str = Field(min_length=2, max_length=100)
    apellido: str = Field(min_length=2, max_length=100)
    correo: EmailStr
    password: str | None = Field(
        default=None,
        min_length=8,
        max_length=128
    )

    model_config = ConfigDict(str_strip_whitespace=True)
