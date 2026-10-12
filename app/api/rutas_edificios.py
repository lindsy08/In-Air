
from fastapi import APIRouter, HTTPException
from pg8000.dbapi import IntegrityError

from app.models.edificios import EdificioCrear, EdificioActualizar
from app.repositories.edificio_repo import (
    listar_edificios,
    crear_edificio,
    obtener_edificio_por_id,
    actualizar_edificio,
    desactivar_edificio
)

router = APIRouter(
    prefix="/edificios",
    tags=["Edificios"]
)


@router.get("/")
def obtener_edificios():
    return listar_edificios()


@router.post("/", status_code=201)
def registrar_edificio(datos: EdificioCrear):
    try:
        edificio = crear_edificio(datos)
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Código duplicado o relación inválida."
        )

    if edificio is None:
        raise HTTPException(
            status_code=404,
            detail="La entidad indicada no existe o está inactiva."
        )

    return edificio


@router.get("/{id_edificio}")
def consultar_edificio(id_edificio: int):
    edificio = obtener_edificio_por_id(id_edificio)

    if edificio is None:
        raise HTTPException(
            status_code=404,
            detail="Edificio no encontrado."
        )

    return edificio


@router.put("/{id_edificio}")
def modificar_edificio(
    id_edificio: int,
    datos: EdificioActualizar
):
    try:
        edificio = actualizar_edificio(id_edificio, datos)
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Código duplicado o relación inválida."
        )

    if edificio is None:
        raise HTTPException(
            status_code=404,
            detail="Edificio no encontrado o entidad inválida."
        )

    return edificio


@router.delete("/{id_edificio}")
def eliminar_edificio(id_edificio: int):
    eliminado = desactivar_edificio(id_edificio)

    if not eliminado:
        raise HTTPException(
            status_code=404,
            detail="Edificio no encontrado o ya desactivado."
        )

    return {
        "mensaje": "Edificio desactivado correctamente."
    }
