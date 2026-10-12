from app.core.database import Database


def obtener_permisos(id_rol, nombre_modulo):
    conexion = Database().get_connection()

    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT mr.puede_ver,
                   mr.puede_crear,
                   mr.puede_editar,
                   mr.puede_eliminar
            FROM moduloxrol mr
            JOIN modulo m
                ON m.id_modulo = mr.id_modulo
            WHERE mr.id_rol = %s
              AND m.nombre = %s
              AND mr.estado = TRUE
              AND m.estado = TRUE
        """, (id_rol, nombre_modulo))

        fila = cursor.fetchone()
        if fila is None:
            return None

        columnas = [col[0] for col in cursor.description]
        return dict(zip(columnas, fila))

    finally:
        conexion.close()