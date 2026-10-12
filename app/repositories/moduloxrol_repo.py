
from app.core.database import Database


def convertir_diccionario(cursor, fila):
    if fila is None:
        return None

    columnas = [col[0] for col in cursor.description]
    return dict(zip(columnas, fila))


def listar_permisos():
    conexion = Database().get_connection()

    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT mr.*,
                   r.nombre AS nombre_rol,
                   m.nombre AS nombre_modulo,
                   m.ruta AS ruta_modulo
            FROM moduloxrol mr
            JOIN rol r
                ON mr.id_rol = r.id_rol
            JOIN modulo m
                ON mr.id_modulo = m.id_modulo
            WHERE mr.estado = TRUE
            ORDER BY mr.id_moduloxrol
        """)

        columnas = [col[0] for col in cursor.description]

        return [
            dict(zip(columnas, fila))
            for fila in cursor.fetchall()
        ]

    finally:
        conexion.close()


def crear_permiso(datos):
    conexion = Database().get_connection()

    try:
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO moduloxrol (
                id_rol,
                id_modulo,
                puede_ver,
                puede_crear,
                puede_editar,
                puede_eliminar
            )
            SELECT r.id_rol,
                   m.id_modulo,
                   %s, %s, %s, %s
            FROM rol r
            CROSS JOIN modulo m
            WHERE r.id_rol = %s
              AND r.estado = TRUE
              AND m.id_modulo = %s
              AND m.estado = TRUE
            RETURNING *
        """, (
            datos.puede_ver,
            datos.puede_crear,
            datos.puede_editar,
            datos.puede_eliminar,
            datos.id_rol,
            datos.id_modulo
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


def obtener_permiso_por_id(id_moduloxrol):
    conexion = Database().get_connection()

    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT *
            FROM moduloxrol
            WHERE id_moduloxrol = %s
              AND estado = TRUE
        """, (id_moduloxrol,))

        return convertir_diccionario(
            cursor, cursor.fetchone()
        )

    finally:
        conexion.close()


def actualizar_permiso(id_moduloxrol, datos):
    conexion = Database().get_connection()

    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE moduloxrol
            SET id_rol = %s,
                id_modulo = %s,
                puede_ver = %s,
                puede_crear = %s,
                puede_editar = %s,
                puede_eliminar = %s
            WHERE id_moduloxrol = %s
              AND estado = TRUE
              AND EXISTS (
                  SELECT 1
                  FROM rol
                  WHERE id_rol = %s
                    AND estado = TRUE
              )
              AND EXISTS (
                  SELECT 1
                  FROM modulo
                  WHERE id_modulo = %s
                    AND estado = TRUE
              )
            RETURNING *
        """, (
            datos.id_rol,
            datos.id_modulo,
            datos.puede_ver,
            datos.puede_crear,
            datos.puede_editar,
            datos.puede_eliminar,
            id_moduloxrol,
            datos.id_rol,
            datos.id_modulo
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


def desactivar_permiso(id_moduloxrol):
    conexion = Database().get_connection()

    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE moduloxrol
            SET estado = FALSE
            WHERE id_moduloxrol = %s
              AND estado = TRUE
            RETURNING id_moduloxrol
        """, (id_moduloxrol,))

        resultado = cursor.fetchone()
        conexion.commit()

        return resultado is not None

    except Exception:
        conexion.rollback()
        raise

    finally:
        conexion.close()
