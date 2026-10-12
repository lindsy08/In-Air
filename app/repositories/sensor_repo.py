
from app.core.database import Database


def convertir_diccionario(cursor, fila):
    if fila is None:
        return None

    columnas = [col[0] for col in cursor.description]
    return dict(zip(columnas, fila))


def listar_sensores():
    conexion = Database().get_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT s.*,
                   d.codigo AS codigo_dispositivo,
                   t.nombre AS tipo_sensor,
                   t.unidad_medida
            FROM sensor s
            JOIN dispositivo d
                ON s.id_dispositivo = d.id_dispositivo
            JOIN tipo_sensor t
                ON s.id_tipo_sensor = t.id_tipo_sensor
            WHERE s.estado = TRUE
            ORDER BY s.id_sensor
        """)

        columnas = [col[0] for col in cursor.description]
        return [
            dict(zip(columnas, fila))
            for fila in cursor.fetchall()
        ]
    finally:
        conexion.close()


def crear_sensor(datos):
    conexion = Database().get_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO sensor (
                id_dispositivo, id_tipo_sensor,
                codigo, modelo
            )
            SELECT d.id_dispositivo,
                   t.id_tipo_sensor,
                   %s, %s
            FROM dispositivo d
            CROSS JOIN tipo_sensor t
            WHERE d.id_dispositivo = %s
              AND d.estado = TRUE
              AND t.id_tipo_sensor = %s
              AND t.estado = TRUE
            RETURNING *
        """, (
            datos.codigo,
            datos.modelo,
            datos.id_dispositivo,
            datos.id_tipo_sensor
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


def obtener_sensor_por_id(id_sensor):
    conexion = Database().get_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT *
            FROM sensor
            WHERE id_sensor = %s AND estado = TRUE
        """, (id_sensor,))

        return convertir_diccionario(
            cursor, cursor.fetchone()
        )
    finally:
        conexion.close()


def actualizar_sensor(id_sensor, datos):
    conexion = Database().get_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE sensor
            SET id_dispositivo = %s,
                id_tipo_sensor = %s,
                codigo = %s,
                modelo = %s
            WHERE id_sensor = %s
              AND estado = TRUE
              AND EXISTS (
                  SELECT 1
                  FROM dispositivo
                  WHERE id_dispositivo = %s
                    AND estado = TRUE
              )
              AND EXISTS (
                  SELECT 1
                  FROM tipo_sensor
                  WHERE id_tipo_sensor = %s
                    AND estado = TRUE
              )
            RETURNING *
        """, (
            datos.id_dispositivo,
            datos.id_tipo_sensor,
            datos.codigo,
            datos.modelo,
            id_sensor,
            datos.id_dispositivo,
            datos.id_tipo_sensor
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


def desactivar_sensor(id_sensor):
    conexion = Database().get_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE sensor
            SET estado = FALSE
            WHERE id_sensor = %s AND estado = TRUE
            RETURNING id_sensor
        """, (id_sensor,))

        resultado = cursor.fetchone()
        conexion.commit()
        return resultado is not None

    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()
