
from fastapi import APIRouter, HTTPException
from pg8000.dbapi import IntegrityError

from app.models.accion_ventilacion import (
    AccionVentilacionCrear,
    AccionVentilacionActualizar
)
from app.repositories.accion_ventilacion_repo import (
    listar_acciones,
    crear_accion,
    obtener_accion_por_id,
    actualizar_accion,
    desactivar_accion
)

router = APIRouter(
    prefix="/acciones-ventilacion",
    tags=["Acciones de ventilación"]
)


@router.get("/")
def obtener_acciones():
    return listar_acciones()


@router.post("/", status_code=201)
def registrar_accion(datos: AccionVentilacionCrear):
    try:
        accion = crear_accion(datos)

    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Código duplicado o datos inválidos."
        )

    if accion is None:
        raise HTTPException(
            status_code=400,
            detail="El salón no existe, está inactivo "
                   "o la alerta no corresponde al salón."
        )

    return accion


@router.get("/{id_accion}")
def consultar_accion(id_accion: int):
    accion = obtener_accion_por_id(id_accion)

    if accion is None:
        raise HTTPException(
            status_code=404,
            detail="Acción de ventilación no encontrada."
        )

    return accion


@router.put("/{id_accion}")
def modificar_accion(
    id_accion: int,
    datos: AccionVentilacionActualizar
):
    try:
        accion = actualizar_accion(id_accion, datos)

    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Código duplicado o datos inválidos."
        )

    if accion is None:
        raise HTTPException(
            status_code=404,
            detail="Acción no encontrada o relaciones inválidas."
        )

    return accion


@router.delete("/{id_accion}")
def eliminar_accion(id_accion: int):
    eliminado = desactivar_accion(id_accion)

    if not eliminado:
        raise HTTPException(
            status_code=404,
            detail="Acción no encontrada o ya desactivada."
        )

    return {
        "mensaje": "Acción de ventilación desactivada correctamente."
    }
