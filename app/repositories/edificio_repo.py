
from app.core.database import Database


def convertir_diccionario(cursor, fila):
    if fila is None:
        return None
    columnas = [col[0] for col in cursor.description]
    return dict(zip(columnas, fila))


def listar_edificios():
    conexion = Database().get_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT e.id_edificio, e.id_entidad,
                   e.nombre, e.codigo, e.numero_pisos,
                   e.estado, e.creado, e.actualizado
            FROM edificio e
            WHERE e.estado = TRUE
            ORDER BY e.id_edificio
        """)
        columnas = [col[0] for col in cursor.description]
        return [
            dict(zip(columnas, fila))
            for fila in cursor.fetchall()
        ]
    finally:
        conexion.close()


def crear_edificio(datos):
    conexion = Database().get_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO edificio (
                id_entidad, nombre, codigo, numero_pisos
            )
            SELECT id_entidad, %s, %s, %s
            FROM entidad
            WHERE id_entidad = %s AND estado = TRUE
            RETURNING *
        """, (
            datos.nombre,
            datos.codigo,
            datos.numero_pisos,
            datos.id_entidad
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


def obtener_edificio_por_id(id_edificio):
    conexion = Database().get_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT *
            FROM edificio
            WHERE id_edificio = %s AND estado = TRUE
        """, (id_edificio,))

        return convertir_diccionario(
            cursor, cursor.fetchone()
        )
    finally:
        conexion.close()


def actualizar_edificio(id_edificio, datos):
    conexion = Database().get_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE edificio
            SET id_entidad = %s,
                nombre = %s,
                codigo = %s,
                numero_pisos = %s
            WHERE id_edificio = %s
              AND estado = TRUE
              AND EXISTS (
                  SELECT 1 FROM entidad
                  WHERE id_entidad = %s AND estado = TRUE
              )
            RETURNING *
        """, (
            datos.id_entidad,
            datos.nombre,
            datos.codigo,
            datos.numero_pisos,
            id_edificio,
            datos.id_entidad
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


def desactivar_edificio(id_edificio):
    conexion = Database().get_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE edificio
            SET estado = FALSE
            WHERE id_edificio = %s AND estado = TRUE
            RETURNING id_edificio
        """, (id_edificio,))

        resultado = cursor.fetchone()
        conexion.commit()
        return resultado is not None

    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()
