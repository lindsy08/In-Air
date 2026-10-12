
from fastapi import APIRouter, HTTPException
from pg8000.dbapi import IntegrityError

from app.models.tipo_sensor import (
    TipoSensorCrear,
    TipoSensorActualizar
)
from app.repositories.tipo_sensor_repo import (
    listar_tipos_sensor,
    crear_tipo_sensor,
    obtener_tipo_sensor_por_id,
    actualizar_tipo_sensor,
    desactivar_tipo_sensor
)

router = APIRouter(
    prefix="/tipos-sensor",
    tags=["Tipos de sensor"]
)


@router.get("/")
def obtener_tipos_sensor():
    return listar_tipos_sensor()


@router.post("/", status_code=201)
def registrar_tipo_sensor(datos: TipoSensorCrear):
    try:
        return crear_tipo_sensor(datos)
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Ya existe un tipo de sensor con ese nombre."
        )


@router.get("/{id_tipo_sensor}")
def consultar_tipo_sensor(id_tipo_sensor: int):
    tipo = obtener_tipo_sensor_por_id(id_tipo_sensor)

    if tipo is None:
        raise HTTPException(
            status_code=404,
            detail="Tipo de sensor no encontrado."
        )

    return tipo


@router.put("/{id_tipo_sensor}")
def modificar_tipo_sensor(
    id_tipo_sensor: int,
    datos: TipoSensorActualizar
):
    try:
        tipo = actualizar_tipo_sensor(
            id_tipo_sensor, datos
        )
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Ya existe un tipo de sensor con ese nombre."
        )

    if tipo is None:
        raise HTTPException(
            status_code=404,
            detail="Tipo de sensor no encontrado."
        )

    return tipo


@router.delete("/{id_tipo_sensor}")
def eliminar_tipo_sensor(id_tipo_sensor: int):
    eliminado = desactivar_tipo_sensor(id_tipo_sensor)

    if not eliminado:
        raise HTTPException(
            status_code=404,
            detail="Tipo de sensor no encontrado o ya desactivado."
        )

    return {
        "mensaje": "Tipo de sensor desactivado correctamente."
    }
