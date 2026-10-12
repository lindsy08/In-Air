
from fastapi import APIRouter, HTTPException
from pg8000.dbapi import IntegrityError

from app.models.salon import SalonCrear, SalonActualizar
from app.repositories.salon_repo import (
    listar_salones,
    crear_salon,
    obtener_salon_por_id,
    actualizar_salon,
    desactivar_salon
)

router = APIRouter(
    prefix="/salones",
    tags=["Salones"]
)


@router.get("/")
def obtener_salones():
    return listar_salones()


@router.post("/", status_code=201)
def registrar_salon(datos: SalonCrear):
    try:
        salon = crear_salon(datos)
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Código duplicado o relación inválida."
        )

    if salon is None:
        raise HTTPException(
            status_code=404,
            detail="El edificio no existe o está inactivo."
        )

    return salon


@router.get("/{id_salon}")
def consultar_salon(id_salon: int):
    salon = obtener_salon_por_id(id_salon)

    if salon is None:
        raise HTTPException(
            status_code=404,
            detail="Salón no encontrado."
        )

    return salon


@router.put("/{id_salon}")
def modificar_salon(
    id_salon: int,
    datos: SalonActualizar
):
    try:
        salon = actualizar_salon(id_salon, datos)
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Código duplicado o relación inválida."
        )

    if salon is None:
        raise HTTPException(
            status_code=404,
            detail="Salón no encontrado o edificio inválido."
        )

    return salon


@router.delete("/{id_salon}")
def eliminar_salon(id_salon: int):
    eliminado = desactivar_salon(id_salon)

    if not eliminado:
        raise HTTPException(
            status_code=404,
            detail="Salón no encontrado o ya desactivado."
        )

    return {
        "mensaje": "Salón desactivado correctamente."
    }
