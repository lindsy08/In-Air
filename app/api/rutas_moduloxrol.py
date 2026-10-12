
from fastapi import APIRouter, HTTPException
from pg8000.dbapi import IntegrityError

from app.models.moduloxrol import (
    ModuloXRolCrear,
    ModuloXRolActualizar
)
from app.repositories.moduloxrol_repo import (
    listar_permisos,
    crear_permiso,
    obtener_permiso_por_id,
    actualizar_permiso,
    desactivar_permiso
)

router = APIRouter(
    prefix="/moduloxrol",
    tags=["Módulos por rol"]
)


@router.get("/")
def obtener_permisos():
    return listar_permisos()


@router.post("/", status_code=201)
def registrar_permiso(datos: ModuloXRolCrear):
    try:
        permiso = crear_permiso(datos)

    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Ya existe una relación entre ese rol "
                   "y módulo, o hay datos inválidos."
        )

    if permiso is None:
        raise HTTPException(
            status_code=404,
            detail="El rol o el módulo no existe "
                   "o está inactivo."
        )

    return permiso


@router.get("/{id_moduloxrol}")
def consultar_permiso(id_moduloxrol: int):
    permiso = obtener_permiso_por_id(id_moduloxrol)

    if permiso is None:
        raise HTTPException(
            status_code=404,
            detail="Permiso no encontrado."
        )

    return permiso


@router.put("/{id_moduloxrol}")
def modificar_permiso(
    id_moduloxrol: int,
    datos: ModuloXRolActualizar
):
    try:
        permiso = actualizar_permiso(
            id_moduloxrol, datos
        )

    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Relación duplicada o datos inválidos."
        )

    if permiso is None:
        raise HTTPException(
            status_code=404,
            detail="Permiso no encontrado o "
                   "rol y módulo inválidos."
        )

    return permiso


@router.delete("/{id_moduloxrol}")
def eliminar_permiso(id_moduloxrol: int):
    eliminado = desactivar_permiso(id_moduloxrol)

    if not eliminado:
        raise HTTPException(
            status_code=404,
            detail="Permiso no encontrado o ya desactivado."
        )

    return {
        "mensaje": "Permiso desactivado correctamente."
    }
