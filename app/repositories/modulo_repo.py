
from app.core.database import Database


def convertir_diccionario(cursor, fila):
    if fila is None:
        return None

    columnas = [col[0] for col in cursor.description]
    return dict(zip(columnas, fila))


def listar_modulos():
    conexion = Database().get_connection()

    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT *
            FROM modulo
            WHERE estado = TRUE
            ORDER BY id_modulo
        """)

        columnas = [col[0] for col in cursor.description]

        return [
            dict(zip(columnas, fila))
            for fila in cursor.fetchall()
        ]

    finally:
        conexion.close()


def crear_modulo(datos):
    conexion = Database().get_connection()

    try:
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO modulo (
                nombre,
                ruta,
                descripcion
            )
            VALUES (%s, %s, %s)
            RETURNING *
        """, (
            datos.nombre,
            datos.ruta,
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


def obtener_modulo_por_id(id_modulo):
    conexion = Database().get_connection()

    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT *
            FROM modulo
            WHERE id_modulo = %s
              AND estado = TRUE
        """, (id_modulo,))

        return convertir_diccionario(
            cursor, cursor.fetchone()
        )

    finally:
        conexion.close()


def actualizar_modulo(id_modulo, datos):
    conexion = Database().get_connection()

    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE modulo
            SET nombre = %s,
                ruta = %s,
                descripcion = %s
            WHERE id_modulo = %s
              AND estado = TRUE
            RETURNING *
        """, (
            datos.nombre,
            datos.ruta,
            datos.descripcion,
            id_modulo
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


def desactivar_modulo(id_modulo):
    conexion = Database().get_connection()

    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE modulo
            SET estado = FALSE
            WHERE id_modulo = %s
              AND estado = TRUE
            RETURNING id_modulo
        """, (id_modulo,))

        resultado = cursor.fetchone()
        conexion.commit()

        return resultado is not None

    except Exception:
        conexion.rollback()
        raise

    finally:
        conexion.close()
