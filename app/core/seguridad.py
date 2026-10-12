import os
import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from pwdlib import PasswordHash

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
EXPIRA_MINUTOS = 60

if not SECRET_KEY:
    raise RuntimeError("Falta la variable de entorno SECRET_KEY")

password_hash = PasswordHash.recommended()


def generar_hash(password: str) -> str:
    return password_hash.hash(password)


def verificar_password(password: str, hash_guardado: str) -> bool:
    return password_hash.verify(password, hash_guardado)


def crear_token(id_usuario: int, id_rol: int) -> str:
    payload = {
        "sub": str(id_usuario),
        "rol": id_rol,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=EXPIRA_MINUTOS),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decodificar_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])