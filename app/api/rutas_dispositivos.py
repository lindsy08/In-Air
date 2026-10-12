
from fastapi import APIRouter, HTTPException
from pg8000.dbapi import IntegrityError

from app.models.dispositivo import (
    DispositivoCrear,
    DispositivoActualizar
)
from app.repositories.dispositivo_repo import (
    listar_dispositivos,
    crear_dispositivo,
    obtener_dispositivo_por_id,
    actualizar_dispositivo,
    desactivar_dispositivo
)

router = APIRouter(
    prefix="/dispositivos",
    tags=["Dispositivos"]
)


@router.get("/")
def obtener_dispositivos():
    return listar_dispositivos()


@router.post("/", status_code=201)
def registrar_dispositivo(datos: DispositivoCrear):
    try:
        dispositivo = crear_dispositivo(datos)
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Código duplicado o relación inválida."
        )

    if dispositivo is None:
        raise HTTPException(
            status_code=404,
            detail="El salón no existe o está inactivo."
        )

    return dispositivo


@router.get("/{id_dispositivo}")
def consultar_dispositivo(id_dispositivo: int):
    dispositivo = obtener_dispositivo_por_id(id_dispositivo)

    if dispositivo is None:
        raise HTTPException(
            status_code=404,
            detail="Dispositivo no encontrado."
        )

    return dispositivo


@router.put("/{id_dispositivo}")
def modificar_dispositivo(
    id_dispositivo: int,
    datos: DispositivoActualizar
):
    try:
        dispositivo = actualizar_dispositivo(
            id_dispositivo, datos
        )
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Código duplicado o relación inválida."
        )

    if dispositivo is None:
        raise HTTPException(
            status_code=404,
            detail="Dispositivo no encontrado o salón inválido."
        )

    return dispositivo


@router.delete("/{id_dispositivo}")
def eliminar_dispositivo(id_dispositivo: int):
    eliminado = desactivar_dispositivo(id_dispositivo)

    if not eliminado:
        raise HTTPException(
            status_code=404,
            detail="Dispositivo no encontrado o ya desactivado."
        )

    return {
        "mensaje": "Dispositivo desactivado correctamente."
    }
