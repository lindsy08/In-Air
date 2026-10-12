
from fastapi import APIRouter, HTTPException
from pg8000.dbapi import IntegrityError

from app.models.sensor import SensorCrear, SensorActualizar
from app.repositories.sensor_repo import (
    listar_sensores,
    crear_sensor,
    obtener_sensor_por_id,
    actualizar_sensor,
    desactivar_sensor
)

router = APIRouter(
    prefix="/sensores",
    tags=["Sensores"]
)


@router.get("/")
def obtener_sensores():
    return listar_sensores()


@router.post("/", status_code=201)
def registrar_sensor(datos: SensorCrear):
    try:
        sensor = crear_sensor(datos)
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Código duplicado o relación inválida."
        )

    if sensor is None:
        raise HTTPException(
            status_code=404,
            detail="Dispositivo o tipo de sensor inexistente o inactivo."
        )

    return sensor


@router.get("/{id_sensor}")
def consultar_sensor(id_sensor: int):
    sensor = obtener_sensor_por_id(id_sensor)

    if sensor is None:
        raise HTTPException(
            status_code=404,
            detail="Sensor no encontrado."
        )

    return sensor


@router.put("/{id_sensor}")
def modificar_sensor(
    id_sensor: int,
    datos: SensorActualizar
):
    try:
        sensor = actualizar_sensor(id_sensor, datos)
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Código duplicado o relación inválida."
        )

    if sensor is None:
        raise HTTPException(
            status_code=404,
            detail="Sensor no encontrado o relaciones inválidas."
        )

    return sensor


@router.delete("/{id_sensor}")
def eliminar_sensor(id_sensor: int):
    eliminado = desactivar_sensor(id_sensor)

    if not eliminado:
        raise HTTPException(
            status_code=404,
            detail="Sensor no encontrado o ya desactivado."
        )

    return {
        "mensaje": "Sensor desactivado correctamente."
    }
