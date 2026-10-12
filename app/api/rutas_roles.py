
from fastapi import APIRouter, HTTPException
from pg8000.dbapi import IntegrityError

from app.models.rol import RolCrear, RolActualizar
from app.repositories.rol_repo import (
    listar_roles,
    crear_rol,
    obtener_rol_por_id,
    actualizar_rol,
    desactivar_rol
)

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.get("/")
def obtener_roles():
    return listar_roles()


@router.post("/", status_code=201)
def registrar_rol(datos: RolCrear):
    try:
        return crear_rol(datos.nombre, datos.descripcion)
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Ya existe un rol con ese nombre."
        )


@router.get("/{id_rol}")
def consultar_rol(id_rol: int):
    rol = obtener_rol_por_id(id_rol)

    if rol is None:
        raise HTTPException(
            status_code=404,
            detail="Rol no encontrado."
        )

    return rol


@router.put("/{id_rol}")
def modificar_rol(id_rol: int, datos: RolActualizar):
    try:
        rol = actualizar_rol(
            id_rol,
            datos.nombre,
            datos.descripcion
        )
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Ya existe un rol con ese nombre."
        )

    if rol is None:
        raise HTTPException(
            status_code=404,
            detail="Rol no encontrado."
        )

    return rol


@router.delete("/{id_rol}")
def eliminar_rol(id_rol: int):
    eliminado = desactivar_rol(id_rol)

    if not eliminado:
        raise HTTPException(
            status_code=404,
            detail="Rol no encontrado o ya desactivado."
        )

    return {
        "mensaje": "Rol desactivado correctamente."
    }
