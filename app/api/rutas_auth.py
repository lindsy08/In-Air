from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.core.seguridad import verificar_password, crear_token
from app.core.dependencias import get_usuario_actual
from app.repositories.usuario_repo import obtener_usuario_para_login

router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"]
)


@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    # En el formulario de OAuth2, "username" es el correo
    usuario = obtener_usuario_para_login(form.username)

    if usuario is None or not verificar_password(
        form.password, usuario["password_hash"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Correo o contraseña incorrectos.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token = crear_token(usuario["id_usuario"], usuario["id_rol"])

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/me")
def quien_soy(usuario=Depends(get_usuario_actual)):
    return usuario