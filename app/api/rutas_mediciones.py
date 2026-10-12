
from fastapi import APIRouter, HTTPException
from pg8000.dbapi import IntegrityError

from app.models.medicion import (
    MedicionCrear,
    MedicionActualizar
)
from app.repositories.medicion_repo import (
    listar_mediciones,
    crear_medicion,
    obtener_medicion_por_id,
    actualizar_medicion,
    desactivar_medicion
)

router = APIRouter(
    prefix="/mediciones",
    tags=["Mediciones"]
)


@router.get("/")
def obtener_mediciones():
    return listar_mediciones()


@router.post("/", status_code=201)
def registrar_medicion(datos: MedicionCrear):
    try:
        medicion = crear_medicion(datos)
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Ya existe una medición para ese sensor "
                   "en esa fecha y hora, o hay datos inválidos."
        )

    if medicion is None:
        raise HTTPException(
            status_code=404,
            detail="Sensor o usuario inexistente o inactivo."
        )

    return medicion


@router.get("/{id_medicion}")
def consultar_medicion(id_medicion: int):
    medicion = obtener_medicion_por_id(id_medicion)

    if medicion is None:
        raise HTTPException(
            status_code=404,
            detail="Medición no encontrada."
        )

    return medicion


@router.put("/{id_medicion}")
def modificar_medicion(
    id_medicion: int,
    datos: MedicionActualizar
):
    try:
        medicion = actualizar_medicion(
            id_medicion, datos
        )
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Fecha y sensor duplicados o datos inválidos."
        )

    if medicion is None:
        raise HTTPException(
            status_code=404,
            detail="Medición no encontrada o relaciones inválidas."
        )

    return medicion


@router.delete("/{id_medicion}")
def eliminar_medicion(id_medicion: int):
    eliminado = desactivar_medicion(id_medicion)

    if not eliminado:
        raise HTTPException(
            status_code=404,
            detail="Medición no encontrada o ya desactivada."
        )

    return {
        "mensaje": "Medición desactivada correctamente."
    }
