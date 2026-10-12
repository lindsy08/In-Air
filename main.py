from fastapi import FastAPI, HTTPException, Depends
from app.core.database import Database
from app.core.dependencias import require_modulo
from app.api.rutas_auth import router as auth_router
from app.api.rutas_roles import router as roles_router
from app.api.rutas_entidades import router as entidades_router
from app.api.rutas_edificios import router as edificios_router
from app.api.rutas_salones import router as salones_router
from app.api.rutas_dispositivos import router as dispositivos_router
from app.api.rutas_tipos_sensor import router as tipos_sensor_router
from app.api.rutas_sensores import router as sensores_router
from app.api.rutas_mediciones import router as mediciones_router
from app.api.rutas_umbrales import router as umbrales_router
from app.api.rutas_alertas import router as alertas_router
from app.api.rutas_acciones_ventilacion import router as acciones_ventilacion_router
from app.api.rutas_modulos import router as modulos_router
from app.api.rutas_moduloxrol import router as moduloxrol_router
from app.api.rutas_usuarios import router as usuarios_router

app = FastAPI(
    title="In-air API",
    description="Sistema de monitoreo de calidad del aire interior",
    version="1.0.0"
)


@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a In-air",
        "estado": "API funcionando correctamente"
    }


@app.get("/probar-conexion", tags=["Pruebas"])
def probar_conexion():
    conexion = None

    try:
        db = Database()
        conexion = db.get_connection()

        cursor = conexion.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_type = 'BASE TABLE'
        """)

        resultado = cursor.fetchone()
        cursor.close()

        return {
            "mensaje": "Conexión exitosa con PostgreSQL",
            "total_tablas": resultado[0]
        }

    except Exception as error:
        print("ERROR DE CONEXION:", type(error).__name__, str(error))

        raise HTTPException(
            status_code=503,
            detail="No fue posible conectar con PostgreSQL"
        )

    finally:
        if conexion is not None:
            conexion.close()


# Login: sin protección
app.include_router(auth_router)

# Resto de módulos: protegidos con JWT + permisos por módulo
app.include_router(roles_router, dependencies=[Depends(require_modulo("roles"))])
app.include_router(entidades_router, dependencies=[Depends(require_modulo("entidades"))])
app.include_router(edificios_router, dependencies=[Depends(require_modulo("edificios"))])
app.include_router(salones_router, dependencies=[Depends(require_modulo("salones"))])
app.include_router(dispositivos_router, dependencies=[Depends(require_modulo("dispositivos"))])
app.include_router(tipos_sensor_router, dependencies=[Depends(require_modulo("tipos_sensor"))])
app.include_router(sensores_router, dependencies=[Depends(require_modulo("sensores"))])
app.include_router(mediciones_router, dependencies=[Depends(require_modulo("mediciones"))])
app.include_router(umbrales_router, dependencies=[Depends(require_modulo("umbrales"))])
app.include_router(alertas_router, dependencies=[Depends(require_modulo("alertas"))])
app.include_router(acciones_ventilacion_router, dependencies=[Depends(require_modulo("acciones_ventilacion"))])
app.include_router(modulos_router, dependencies=[Depends(require_modulo("modulos"))])
app.include_router(moduloxrol_router, dependencies=[Depends(require_modulo("moduloxrol"))])
app.include_router(usuarios_router, dependencies=[Depends(require_modulo("usuarios"))])