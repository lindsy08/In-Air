
from fastapi import APIRouter, HTTPException
from pg8000.dbapi import IntegrityError

from app.models.umbral import (
    UmbralCrear,
    UmbralActualizar
)
from app.repositories.umbral_repo import (
    listar_umbrales,
    crear_umbral,
    obtener_umbral_por_id,
    actualizar_umbral,
    desactivar_umbral
)

router = APIRouter(
    prefix="/umbrales",
    tags=["Umbrales"]
)


@router.get("/")
def obtener_umbrales():
    return listar_umbrales()


@router.post("/", status_code=201)
def registrar_umbral(datos: UmbralCrear):
    try:
        umbral = crear_umbral(datos)
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Ya existe un umbral para ese salón "
                   "y tipo de sensor, o hay datos inválidos."
        )

    if umbral is None:
        raise HTTPException(
            status_code=404,
            detail="Salón o tipo de sensor inexistente o inactivo."
        )

    return umbral


@router.get("/{id_umbral}")
def consultar_umbral(id_umbral: int):
    umbral = obtener_umbral_por_id(id_umbral)

    if umbral is None:
        raise HTTPException(
            status_code=404,
            detail="Umbral no encontrado."
        )

    return umbral


@router.put("/{id_umbral}")
def modificar_umbral(
    id_umbral: int,
    datos: UmbralActualizar
):
    try:
        umbral = actualizar_umbral(id_umbral, datos)
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Ya existe un umbral para ese salón "
                   "y tipo de sensor, o hay datos inválidos."
        )

    if umbral is None:
        raise HTTPException(
            status_code=404,
            detail="Umbral no encontrado o relaciones inválidas."
        )

    return umbral


@router.delete("/{id_umbral}")
def eliminar_umbral(id_umbral: int):
    eliminado = desactivar_umbral(id_umbral)

    if not eliminado:
        raise HTTPException(
            status_code=404,
            detail="Umbral no encontrado o ya desactivado."
        )

    return {
        "mensaje": "Umbral desactivado correctamente."
    }
