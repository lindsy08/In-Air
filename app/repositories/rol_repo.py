
from app.core.database import Database


def listar_roles():
    conexion = Database().get_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT id_rol, nombre, descripcion, estado
            FROM rol
            WHERE estado = TRUE
            ORDER BY id_rol
        """)
        columnas = [col[0] for col in cursor.description]
        return [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
    finally:
        conexion.close()


def crear_rol(nombre, descripcion):
    conexion = Database().get_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO rol (nombre, descripcion)
            VALUES (%s, %s)
            RETURNING id_rol, nombre, descripcion, estado
        """, (nombre, descripcion))
        fila = cursor.fetchone()
        columnas = [col[0] for col in cursor.description]
        conexion.commit()
        return dict(zip(columnas, fila))
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()

def obtener_rol_por_id(id_rol):
    conexion = Database().get_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT id_rol, nombre, descripcion, estado
            FROM rol
            WHERE id_rol = %s AND estado = TRUE
        """, (id_rol,))

        fila = cursor.fetchone()

        if fila is None:
            return None

        columnas = [col[0] for col in cursor.description]
        return dict(zip(columnas, fila))
    finally:
        conexion.close()


def actualizar_rol(id_rol, nombre, descripcion):
    conexion = Database().get_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE rol
            SET nombre = %s, descripcion = %s
            WHERE id_rol = %s AND estado = TRUE
            RETURNING id_rol, nombre, descripcion, estado
        """, (nombre, descripcion, id_rol))

        fila = cursor.fetchone()

        if fila is None:
            conexion.rollback()
            return None

        columnas = [col[0] for col in cursor.description]
        conexion.commit()
        return dict(zip(columnas, fila))

    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()


def desactivar_rol(id_rol):
    conexion = Database().get_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE rol
            SET estado = FALSE
            WHERE id_rol = %s AND estado = TRUE
            RETURNING id_rol
        """, (id_rol,))

        fila = cursor.fetchone()

        if fila is None:
            conexion.rollback()
            return False

        conexion.commit()
        return True

    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()
