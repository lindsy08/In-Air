
from fastapi import APIRouter, HTTPException
from pg8000.dbapi import IntegrityError

from app.models.alerta import (
    AlertaCrear,
    AlertaActualizar
)
from app.repositories.alerta_repo import (
    listar_alertas,
    crear_alerta,
    obtener_alerta_por_id,
    actualizar_alerta,
    desactivar_alerta
)

router = APIRouter(
    prefix="/alertas",
    tags=["Alertas"]
)


@router.get("/")
def obtener_alertas():
    return listar_alertas()


@router.post("/", status_code=201)
def registrar_alerta(datos: AlertaCrear):
    try:
        alerta = crear_alerta(datos)

    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Ya existe una alerta para esa medición "
                   "y umbral, o hay datos inválidos."
        )

    if alerta is None:
        raise HTTPException(
            status_code=400,
            detail="La medición y el umbral no son "
                   "compatibles, están inactivos o el "
                   "valor está dentro del rango."
        )

    return alerta


@router.get("/{id_alerta}")
def consultar_alerta(id_alerta: int):
    alerta = obtener_alerta_por_id(id_alerta)

    if alerta is None:
        raise HTTPException(
            status_code=404,
            detail="Alerta no encontrada."
        )

    return alerta


@router.put("/{id_alerta}")
def modificar_alerta(
    id_alerta: int,
    datos: AlertaActualizar
):
    try:
        alerta = actualizar_alerta(
            id_alerta, datos
        )

    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Alerta duplicada o datos inválidos."
        )

    if alerta is None:
        raise HTTPException(
            status_code=404,
            detail="Alerta no encontrada o "
                   "medición y umbral incompatibles."
        )

    return alerta


@router.delete("/{id_alerta}")
def eliminar_alerta(id_alerta: int):
    eliminado = desactivar_alerta(id_alerta)

    if not eliminado:
        raise HTTPException(
            status_code=404,
            detail="Alerta no encontrada o ya desactivada."
        )

    return {
        "mensaje": "Alerta desactivada correctamente."
    }
