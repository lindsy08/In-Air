import jwt
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer

from app.core.seguridad import decodificar_token
from app.repositories.usuario_repo import obtener_usuario_por_id
from app.repositories.permiso_repo import obtener_permisos

oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/login")

PERMISO_POR_METODO = {
    "GET": "puede_ver",
    "POST": "puede_crear",
    "PUT": "puede_editar",
    "PATCH": "puede_editar",
    "DELETE": "puede_eliminar",
}


def get_usuario_actual(token: str = Depends(oauth2)):
    try:
        datos = decodificar_token(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="El token ha expirado.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido.")

    usuario = obtener_usuario_por_id(int(datos["sub"]))

    if usuario is None:
        raise HTTPException(
            status_code=401,
            detail="Usuario no válido o desactivado."
        )

    return usuario


def require_modulo(nombre_modulo: str):
    def verificador(
        request: Request,
        usuario=Depends(get_usuario_actual)
    ):
        permisos = obtener_permisos(usuario["id_rol"], nombre_modulo)
        columna = PERMISO_POR_METODO.get(request.method)

        if permisos is None or not permisos.get(columna):
            raise HTTPException(
                status_code=403,
                detail="No tienes permiso para esta acción en este módulo."
            )

        return usuario

    return verificador