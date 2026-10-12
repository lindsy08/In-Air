
from fastapi import FastAPI, HTTPException
from app.core.database import Database
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

app.include_router(roles_router)
app.include_router(entidades_router)
app.include_router(edificios_router)
app.include_router(salones_router)
app.include_router(dispositivos_router)
app.include_router(tipos_sensor_router)
app.include_router(sensores_router)
app.include_router(mediciones_router)
app.include_router(umbrales_router)
app.include_router(alertas_router)
app.include_router(acciones_ventilacion_router)
app.include_router(modulos_router)
app.include_router(moduloxrol_router)
app.include_router(usuarios_router)