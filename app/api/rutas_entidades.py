    
from fastapi import APIRouter, HTTPException
from pg8000.dbapi import IntegrityError

from app.models.entidad import EntidadCrear, EntidadActualizar
from app.repositories.entidad_repo import (
    listar_entidades,
    crear_entidad,
    obtener_entidad_por_id,
    actualizar_entidad,
    desactivar_entidad
)

router = APIRouter(
    prefix="/entidades",
    tags=["Entidades"]
)


@router.get("/")
def obtener_entidades():
    return listar_entidades()


@router.post("/", status_code=201)
def registrar_entidad(datos: EntidadCrear):
    try:
        return crear_entidad(datos)
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Ya existe una entidad con ese código."
        )


@router.get("/{id_entidad}")
def consultar_entidad(id_entidad: int):
    entidad = obtener_entidad_por_id(id_entidad)

    if entidad is None:
        raise HTTPException(
            status_code=404,
            detail="Entidad no encontrada."
        )

    return entidad


@router.put("/{id_entidad}")
def modificar_entidad(
    id_entidad: int,
    datos: EntidadActualizar
):
    try:
        entidad = actualizar_entidad(id_entidad, datos)
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Ya existe una entidad con ese código."
        )

    if entidad is None:
        raise HTTPException(
            status_code=404,
            detail="Entidad no encontrada."
        )

    return entidad


@router.delete("/{id_entidad}")
def eliminar_entidad(id_entidad: int):
    eliminado = desactivar_entidad(id_entidad)

    if not eliminado:
        raise HTTPException(
            status_code=404,
            detail="Entidad no encontrada o ya desactivada."
        )

    return {
        "mensaje": "Entidad desactivada correctamente."
    }
