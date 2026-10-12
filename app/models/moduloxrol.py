
from pydantic import BaseModel, Field


class ModuloXRolCrear(BaseModel):
    id_rol: int = Field(gt=0)
    id_modulo: int = Field(gt=0)

    puede_ver: bool = True
    puede_crear: bool = False
    puede_editar: bool = False
    puede_eliminar: bool = False


class ModuloXRolActualizar(ModuloXRolCrear):
    pass
