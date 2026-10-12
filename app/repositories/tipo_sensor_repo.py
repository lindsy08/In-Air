
from app.core.database import Database


def convertir_diccionario(cursor, fila):
    if fila is None:
        return None

    columnas = [col[0] for col in cursor.description]
    return dict(zip(columnas, fila))


def listar_tipos_sensor():
    conexion = Database().get_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT *
            FROM tipo_sensor
            WHERE estado = TRUE
            ORDER BY id_tipo_sensor
        """)

        columnas = [col[0] for col in cursor.description]
        return [
            dict(zip(columnas, fila))
            for fila in cursor.fetchall()
        ]
    finally:
        conexion.close()


def crear_tipo_sensor(datos):
    conexion = Database().get_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO tipo_sensor (
                nombre, unidad_medida, descripcion
            )
            VALUES (%s, %s, %s)
            RETURNING *
        """, (
            datos.nombre,
            datos.unidad_medida,
            datos.descripcion
        ))

        resultado = convertir_diccionario(
            cursor, cursor.fetchone()
        )
        conexion.commit()
        return resultado

    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()


def obtener_tipo_sensor_por_id(id_tipo_sensor):
    conexion = Database().get_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT *
            FROM tipo_sensor
            WHERE id_tipo_sensor = %s
              AND estado = TRUE
        """, (id_tipo_sensor,))

        return convertir_diccionario(
            cursor, cursor.fetchone()
        )
    finally:
        conexion.close()


def actualizar_tipo_sensor(id_tipo_sensor, datos):
    conexion = Database().get_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE tipo_sensor
            SET nombre = %s,
                unidad_medida = %s,
                descripcion = %s
            WHERE id_tipo_sensor = %s
              AND estado = TRUE
            RETURNING *
        """, (
            datos.nombre,
            datos.unidad_medida,
            datos.descripcion,
            id_tipo_sensor
        ))

        resultado = convertir_diccionario(
            cursor, cursor.fetchone()
        )
        conexion.commit()
        return resultado

    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()


def desactivar_tipo_sensor(id_tipo_sensor):
    conexion = Database().get_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE tipo_sensor
            SET estado = FALSE
            WHERE id_tipo_sensor = %s
              AND estado = TRUE
            RETURNING id_tipo_sensor
        """, (id_tipo_sensor,))

        resultado = cursor.fetchone()
        conexion.commit()
        return resultado is not None

    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()
