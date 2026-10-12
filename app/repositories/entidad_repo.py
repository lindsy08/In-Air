
from app.core.database import Database


def convertir_diccionario(cursor, fila):
    if fila is None:
        return None

    columnas = [col[0] for col in cursor.description]
    return dict(zip(columnas, fila))


def listar_entidades():
    conexion = Database().get_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT id_entidad, nombre, codigo, tipo_entidad,
                   direccion, correo_contacto, estado,
                   creado, actualizado
            FROM entidad
            WHERE estado = TRUE
            ORDER BY id_entidad
        """)
        columnas = [col[0] for col in cursor.description]
        return [
            dict(zip(columnas, fila))
            for fila in cursor.fetchall()
        ]
    finally:
        conexion.close()


def crear_entidad(datos):
    conexion = Database().get_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO entidad (
                nombre, codigo, tipo_entidad,
                direccion, correo_contacto
            )
            VALUES (%s, %s, %s, %s, %s)
            RETURNING *
        """, (
            datos.nombre,
            datos.codigo,
            datos.tipo_entidad,
            datos.direccion,
            datos.correo_contacto
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


def obtener_entidad_por_id(id_entidad):
    conexion = Database().get_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT *
            FROM entidad
            WHERE id_entidad = %s AND estado = TRUE
        """, (id_entidad,))

        return convertir_diccionario(
            cursor, cursor.fetchone()
        )
    finally:
        conexion.close()


def actualizar_entidad(id_entidad, datos):
    conexion = Database().get_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE entidad
            SET nombre = %s,
                codigo = %s,
                tipo_entidad = %s,
                direccion = %s,
                correo_contacto = %s
            WHERE id_entidad = %s AND estado = TRUE
            RETURNING *
        """, (
            datos.nombre,
            datos.codigo,
            datos.tipo_entidad,
            datos.direccion,
            datos.correo_contacto,
            id_entidad
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


def desactivar_entidad(id_entidad):
    conexion = Database().get_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE entidad
            SET estado = FALSE
            WHERE id_entidad = %s AND estado = TRUE
            RETURNING id_entidad
        """, (id_entidad,))

        resultado = cursor.fetchone()
        conexion.commit()

        return resultado is not None

    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()
