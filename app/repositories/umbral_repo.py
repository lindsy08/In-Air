
from app.core.database import Database


def convertir_diccionario(cursor, fila):
    if fila is None:
        return None

    columnas = [col[0] for col in cursor.description]
    return dict(zip(columnas, fila))


def listar_umbrales():
    conexion = Database().get_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT u.*,
                   t.nombre AS tipo_sensor,
                   t.unidad_medida,
                   s.codigo AS codigo_salon
            FROM umbral u
            JOIN tipo_sensor t
                ON u.id_tipo_sensor = t.id_tipo_sensor
            JOIN salon s
                ON u.id_salon = s.id_salon
            WHERE u.estado = TRUE
            ORDER BY u.id_umbral
        """)

        columnas = [col[0] for col in cursor.description]
        return [
            dict(zip(columnas, fila))
            for fila in cursor.fetchall()
        ]
    finally:
        conexion.close()


def crear_umbral(datos):
    conexion = Database().get_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO umbral (
                id_tipo_sensor,
                id_salon,
                valor_minimo,
                valor_maximo,
                descripcion
            )
            SELECT t.id_tipo_sensor,
                   s.id_salon,
                   %s, %s, %s
            FROM tipo_sensor t
            CROSS JOIN salon s
            WHERE t.id_tipo_sensor = %s
              AND t.estado = TRUE
              AND s.id_salon = %s
              AND s.estado = TRUE
            RETURNING *
        """, (
            datos.valor_minimo,
            datos.valor_maximo,
            datos.descripcion,
            datos.id_tipo_sensor,
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


def obtener_umbral_por_id(id_umbral):
    conexion = Database().get_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT *
            FROM umbral
            WHERE id_umbral = %s
              AND estado = TRUE
        """, (id_umbral,))

        return convertir_diccionario(
            cursor, cursor.fetchone()
        )
    finally:
        conexion.close()


def actualizar_umbral(id_umbral, datos):
    conexion = Database().get_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE umbral
            SET id_tipo_sensor = %s,
                id_salon = %s,
                valor_minimo = %s,
                valor_maximo = %s,
                descripcion = %s
            WHERE id_umbral = %s
              AND estado = TRUE
              AND EXISTS (
                  SELECT 1
                  FROM tipo_sensor
                  WHERE id_tipo_sensor = %s
                    AND estado = TRUE
              )
              AND EXISTS (
                  SELECT 1
                  FROM salon
                  WHERE id_salon = %s
                    AND estado = TRUE
              )
            RETURNING *
        """, (
            datos.id_tipo_sensor,
            datos.id_salon,
            datos.valor_minimo,
            datos.valor_maximo,
            datos.descripcion,
            id_umbral,
            datos.id_tipo_sensor,
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


def desactivar_umbral(id_umbral):
    conexion = Database().get_connection()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE umbral
            SET estado = FALSE
            WHERE id_umbral = %s
              AND estado = TRUE
            RETURNING id_umbral
        """, (id_umbral,))

        resultado = cursor.fetchone()
        conexion.commit()
        return resultado is not None

    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()
