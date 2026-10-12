
from app.core.database import Database


def convertir_diccionario(cursor, fila):
    if fila is None:
        return None

    columnas = [col[0] for col in cursor.description]
    return dict(zip(columnas, fila))


def listar_mediciones():
    conexion = Database().get_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT m.*,
                   s.codigo AS codigo_sensor,
                   t.nombre AS tipo_sensor,
                   t.unidad_medida
            FROM medicion m
            JOIN sensor s
                ON m.id_sensor = s.id_sensor
            JOIN tipo_sensor t
                ON s.id_tipo_sensor = t.id_tipo_sensor
            WHERE m.estado = TRUE
            ORDER BY m.fecha_medicion DESC
        """)

        columnas = [col[0] for col in cursor.description]
        return [
            dict(zip(columnas, fila))
            for fila in cursor.fetchall()
        ]
    finally:
        conexion.close()


def crear_medicion(datos):
    conexion = Database().get_connection()
    try:
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO medicion (
                id_sensor,
                id_usuario_registro,
                valor,
                fecha_medicion,
                origen
            )
            SELECT s.id_sensor,
                   %s, %s, %s, %s
            FROM sensor s
            JOIN dispositivo d
                ON s.id_dispositivo = d.id_dispositivo
            WHERE s.id_sensor = %s
              AND s.estado = TRUE
              AND d.estado = TRUE
              AND (
                  %s IS NULL
                  OR EXISTS (
                      SELECT 1
                      FROM usuario u
                      WHERE u.id_usuario = %s
                        AND u.estado = TRUE
                  )
              )
            RETURNING *
        """, (
            datos.id_usuario_registro,
            datos.valor,
            datos.fecha_medicion,
            datos.origen,
            datos.id_sensor,
            datos.id_usuario_registro,
            datos.id_usuario_registro
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


def obtener_medicion_por_id(id_medicion):
    conexion = Database().get_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT *
            FROM medicion
            WHERE id_medicion = %s
              AND estado = TRUE
        """, (id_medicion,))

        return convertir_diccionario(
            cursor, cursor.fetchone()
        )
    finally:
        conexion.close()


def actualizar_medicion(id_medicion, datos):
    conexion = Database().get_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE medicion
            SET id_sensor = %s,
                id_usuario_registro = %s,
                valor = %s,
                fecha_medicion = %s,
                origen = %s
            WHERE id_medicion = %s
              AND estado = TRUE
              AND EXISTS (
                  SELECT 1
                  FROM sensor s
                  JOIN dispositivo d
                    ON s.id_dispositivo = d.id_dispositivo
                  WHERE s.id_sensor = %s
                    AND s.estado = TRUE
                    AND d.estado = TRUE
              )
              AND (
                  %s IS NULL
                  OR EXISTS (
                      SELECT 1
                      FROM usuario u
                      WHERE u.id_usuario = %s
                        AND u.estado = TRUE
                  )
              )
            RETURNING *
        """, (
            datos.id_sensor,
            datos.id_usuario_registro,
            datos.valor,
            datos.fecha_medicion,
            datos.origen,
            id_medicion,
            datos.id_sensor,
            datos.id_usuario_registro,
            datos.id_usuario_registro
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


def desactivar_medicion(id_medicion):
    conexion = Database().get_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE medicion
            SET estado = FALSE
            WHERE id_medicion = %s
              AND estado = TRUE
            RETURNING id_medicion
        """, (id_medicion,))

        resultado = cursor.fetchone()
        conexion.commit()
        return resultado is not None

    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()
