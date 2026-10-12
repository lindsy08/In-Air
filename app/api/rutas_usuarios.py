
from fastapi import APIRouter, HTTPException
from pg8000.dbapi import IntegrityError

from app.models.usuario import (
    UsuarioCrear,
    UsuarioActualizar
)
from app.repositories.usuario_repo import (
    listar_usuarios,
    crear_usuario,
    obtener_usuario_por_id,
    actualizar_usuario,
    desactivar_usuario
)

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)


@router.get("/")
def obtener_usuarios():
    return listar_usuarios()


@router.post("/", status_code=201)
def registrar_usuario(datos: UsuarioCrear):
    try:
        usuario = crear_usuario(datos)

    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="El correo ya está registrado "
                   "o los datos son inválidos."
        )

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="El rol no existe o está inactivo."
        )

    return usuario


@router.get("/{id_usuario}")
def consultar_usuario(id_usuario: int):
    usuario = obtener_usuario_por_id(id_usuario)

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado."
        )

    return usuario


@router.put("/{id_usuario}")
def modificar_usuario(
    id_usuario: int,
    datos: UsuarioActualizar
):
    try:
        usuario = actualizar_usuario(
            id_usuario, datos
        )

    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="El correo ya está registrado "
                   "o los datos son inválidos."
        )

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado o rol inválido."
        )

    return usuario


@router.delete("/{id_usuario}")
def eliminar_usuario(id_usuario: int):
    eliminado = desactivar_usuario(id_usuario)

    if not eliminado:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado o ya desactivado."
        )

    return {
        "mensaje": "Usuario desactivado correctamente."
    }
