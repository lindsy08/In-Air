
from app.core.database import Database


def convertir_diccionario(cursor, fila):
    if fila is None:
        return None

    columnas = [col[0] for col in cursor.description]
    return dict(zip(columnas, fila))


def listar_dispositivos():
    conexion = Database().get_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT d.*, s.codigo AS codigo_salon
            FROM dispositivo d
            JOIN salon s ON d.id_salon = s.id_salon
            WHERE d.estado = TRUE
            ORDER BY d.id_dispositivo
        """)

        columnas = [col[0] for col in cursor.description]
        return [
            dict(zip(columnas, fila))
            for fila in cursor.fetchall()
        ]
    finally:
        conexion.close()


def crear_dispositivo(datos):
    conexion = Database().get_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO dispositivo (
                id_salon, codigo, modelo,
                es_virtual, fecha_instalacion
            )
            SELECT id_salon, %s, %s, %s, %s
            FROM salon
            WHERE id_salon = %s AND estado = TRUE
            RETURNING *
        """, (
            datos.codigo,
            datos.modelo,
            datos.es_virtual,
            datos.fecha_instalacion,
            datos.id_salon
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


def obtener_dispositivo_por_id(id_dispositivo):
    conexion = Database().get_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT *
            FROM dispositivo
            WHERE id_dispositivo = %s AND estado = TRUE
        """, (id_dispositivo,))

        return convertir_diccionario(
            cursor, cursor.fetchone()
        )
    finally:
        conexion.close()


def actualizar_dispositivo(id_dispositivo, datos):
    conexion = Database().get_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE dispositivo
            SET id_salon = %s,
                codigo = %s,
                modelo = %s,
                es_virtual = %s,
                fecha_instalacion = %s
            WHERE id_dispositivo = %s
              AND estado = TRUE
              AND EXISTS (
                  SELECT 1
                  FROM salon
                  WHERE id_salon = %s
                    AND estado = TRUE
              )
            RETURNING *
        """, (
            datos.id_salon,
            datos.codigo,
            datos.modelo,
            datos.es_virtual,
            datos.fecha_instalacion,
            id_dispositivo,
            datos.id_salon
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


def desactivar_dispositivo(id_dispositivo):
    conexion = Database().get_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE dispositivo
            SET estado = FALSE
            WHERE id_dispositivo = %s AND estado = TRUE
            RETURNING id_dispositivo
        """, (id_dispositivo,))

        resultado = cursor.fetchone()
        conexion.commit()
        return resultado is not None

    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()
