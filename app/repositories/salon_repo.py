
from app.core.database import Database


def convertir_diccionario(cursor, fila):
    if fila is None:
        return None

    columnas = [col[0] for col in cursor.description]
    return dict(zip(columnas, fila))


def listar_salones():
    conexion = Database().get_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT s.*, e.nombre AS nombre_edificio
            FROM salon s
            JOIN edificio e ON s.id_edificio = e.id_edificio
            WHERE s.estado = TRUE
            ORDER BY s.id_salon
        """)

        columnas = [col[0] for col in cursor.description]
        return [
            dict(zip(columnas, fila))
            for fila in cursor.fetchall()
        ]
    finally:
        conexion.close()


def crear_salon(datos):
    conexion = Database().get_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO salon (
                id_edificio, codigo, piso,
                capacidad, area_m2, altura_m
            )
            SELECT id_edificio, %s, %s, %s, %s, %s
            FROM edificio
            WHERE id_edificio = %s AND estado = TRUE
            RETURNING *
        """, (
            datos.codigo,
            datos.piso,
            datos.capacidad,
            datos.area_m2,
            datos.altura_m,
            datos.id_edificio
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


def obtener_salon_por_id(id_salon):
    conexion = Database().get_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT *
            FROM salon
            WHERE id_salon = %s AND estado = TRUE
        """, (id_salon,))

        return convertir_diccionario(
            cursor, cursor.fetchone()
        )
    finally:
        conexion.close()


def actualizar_salon(id_salon, datos):
    conexion = Database().get_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE salon
            SET id_edificio = %s,
                codigo = %s,
                piso = %s,
                capacidad = %s,
                area_m2 = %s,
                altura_m = %s
            WHERE id_salon = %s
              AND estado = TRUE
              AND EXISTS (
                  SELECT 1
                  FROM edificio
                  WHERE id_edificio = %s
                    AND estado = TRUE
              )
            RETURNING *
        """, (
            datos.id_edificio,
            datos.codigo,
            datos.piso,
            datos.capacidad,
            datos.area_m2,
            datos.altura_m,
            id_salon,
            datos.id_edificio
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


def desactivar_salon(id_salon):
    conexion = Database().get_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE salon
            SET estado = FALSE
            WHERE id_salon = %s AND estado = TRUE
            RETURNING id_salon
        """, (id_salon,))

        resultado = cursor.fetchone()
        conexion.commit()
        return resultado is not None

    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()
