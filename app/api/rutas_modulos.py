
from fastapi import APIRouter, HTTPException
from pg8000.dbapi import IntegrityError

from app.models.modulo import (
    ModuloCrear,
    ModuloActualizar
)
from app.repositories.modulo_repo import (
    listar_modulos,
    crear_modulo,
    obtener_modulo_por_id,
    actualizar_modulo,
    desactivar_modulo
)

router = APIRouter(
    prefix="/modulos",
    tags=["Módulos"]
)


@router.get("/")
def obtener_modulos():
    return listar_modulos()


@router.post("/", status_code=201)
def registrar_modulo(datos: ModuloCrear):
    try:
        return crear_modulo(datos)

    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Ya existe un módulo con ese nombre "
                   "o esa ruta."
        )


@router.get("/{id_modulo}")
def consultar_modulo(id_modulo: int):
    modulo = obtener_modulo_por_id(id_modulo)

    if modulo is None:
        raise HTTPException(
            status_code=404,
            detail="Módulo no encontrado."
        )

    return modulo


@router.put("/{id_modulo}")
def modificar_modulo(
    id_modulo: int,
    datos: ModuloActualizar
):
    try:
        modulo = actualizar_modulo(
            id_modulo, datos
        )

    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Ya existe un módulo con ese nombre "
                   "o esa ruta."
        )

    if modulo is None:
        raise HTTPException(
            status_code=404,
            detail="Módulo no encontrado."
        )

    return modulo


@router.delete("/{id_modulo}")
def eliminar_modulo(id_modulo: int):
    eliminado = desactivar_modulo(id_modulo)

    if not eliminado:
        raise HTTPException(
            status_code=404,
            detail="Módulo no encontrado o ya desactivado."
        )

    return {
        "mensaje": "Módulo desactivado correctamente."
    }
