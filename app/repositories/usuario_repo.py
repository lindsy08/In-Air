
from app.core.database import Database
from app.core.seguridad import generar_hash


def convertir_diccionario(cursor, fila):
    if fila is None:
        return None

    columnas = [col[0] for col in cursor.description]
    return dict(zip(columnas, fila))


def listar_usuarios():
    conexion = Database().get_connection()

    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT u.id_usuario,
                   u.id_rol,
                   u.nombre,
                   u.apellido,
                   u.correo,
                   u.estado,
                   u.creado,
                   u.actualizado,
                   r.nombre AS nombre_rol
            FROM usuario u
            JOIN rol r
                ON u.id_rol = r.id_rol
            WHERE u.estado = TRUE
            ORDER BY u.id_usuario
        """)

        columnas = [col[0] for col in cursor.description]

        return [
            dict(zip(columnas, fila))
            for fila in cursor.fetchall()
        ]

    finally:
        conexion.close()


def crear_usuario(datos):
    conexion = Database().get_connection()

    try:
        cursor = conexion.cursor()

        hash_password = generar_hash(datos.password)

        cursor.execute("""
            INSERT INTO usuario (
                id_rol,
                nombre,
                apellido,
                correo,
                password_hash
            )
            SELECT r.id_rol,
                   %s, %s, %s, %s
            FROM rol r
            WHERE r.id_rol = %s
              AND r.estado = TRUE
            RETURNING
                id_usuario,
                id_rol,
                nombre,
                apellido,
                correo,
                estado,
                creado,
                actualizado
        """, (
            datos.nombre,
            datos.apellido,
            str(datos.correo),
            hash_password,
            datos.id_rol
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


def obtener_usuario_por_id(id_usuario):
    conexion = Database().get_connection()

    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT id_usuario,
                   id_rol,
                   nombre,
                   apellido,
                   correo,
                   estado,
                   creado,
                   actualizado
            FROM usuario
            WHERE id_usuario = %s
              AND estado = TRUE
        """, (id_usuario,))

        return convertir_diccionario(
            cursor, cursor.fetchone()
        )

    finally:
        conexion.close()


def actualizar_usuario(id_usuario, datos):
    conexion = Database().get_connection()

    try:
        cursor = conexion.cursor()

        nuevo_hash = None

        if datos.password is not None:
            nuevo_hash = generar_hash(datos.password)

        cursor.execute("""
            UPDATE usuario
            SET id_rol = %s,
                nombre = %s,
                apellido = %s,
                correo = %s,
                password_hash = COALESCE(
                    %s, password_hash
                )
            WHERE id_usuario = %s
              AND estado = TRUE
              AND EXISTS (
                  SELECT 1
                  FROM rol
                  WHERE id_rol = %s
                    AND estado = TRUE
              )
            RETURNING
                id_usuario,
                id_rol,
                nombre,
                apellido,
                correo,
                estado,
                creado,
                actualizado
        """, (
            datos.id_rol,
            datos.nombre,
            datos.apellido,
            str(datos.correo),
            nuevo_hash,
            id_usuario,
            datos.id_rol
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


def desactivar_usuario(id_usuario):
    conexion = Database().get_connection()

    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE usuario
            SET estado = FALSE
            WHERE id_usuario = %s
              AND estado = TRUE
            RETURNING id_usuario
        """, (id_usuario,))

        resultado = cursor.fetchone()
        conexion.commit()

        return resultado is not None

    except Exception:
        conexion.rollback()
        raise

    finally:
        conexion.close()

def obtener_usuario_para_login(correo):
    conexion = Database().get_connection()

    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT id_usuario,
                   id_rol,
                   correo,
                   password_hash
            FROM usuario
            WHERE correo = %s
              AND estado = TRUE
        """, (correo,))

        return convertir_diccionario(
            cursor, cursor.fetchone()
        )

    finally:
        conexion.close()