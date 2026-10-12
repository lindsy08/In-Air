
from app.core.database import Database


def convertir_diccionario(cursor, fila):
    if fila is None:
        return None

    columnas = [col[0] for col in cursor.description]
    return dict(zip(columnas, fila))


def listar_acciones():
    conexion = Database().get_connection()

    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT av.*,
                   s.codigo AS codigo_salon,
                   a.nivel AS nivel_alerta,
                   a.mensaje AS mensaje_alerta
            FROM accion_ventilacion av
            JOIN salon s
                ON av.id_salon = s.id_salon
            LEFT JOIN alerta a
                ON av.id_alerta = a.id_alerta
            WHERE av.estado = TRUE
            ORDER BY av.fecha_accion DESC, av.id_accion DESC
        """)

        columnas = [col[0] for col in cursor.description]

        return [
            dict(zip(columnas, fila))
            for fila in cursor.fetchall()
        ]

    finally:
        conexion.close()


def crear_accion(datos):
    conexion = Database().get_connection()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO accion_ventilacion (
                id_salon,
                id_alerta,
                codigo,
                tipo_accion,
                modo,
                fecha_accion,
                observacion
            )
            SELECT s.id_salon,
                   %s, %s, %s, %s,
                   COALESCE(%s, CURRENT_TIMESTAMP),
                   %s
            FROM salon s
            WHERE s.id_salon = %s
              AND s.estado = TRUE
              AND (
                  %s IS NULL
                  OR EXISTS (
                      SELECT 1
                      FROM alerta a
                      JOIN medicion m
                        ON a.id_medicion = m.id_medicion
                      JOIN sensor se
                        ON m.id_sensor = se.id_sensor
                      JOIN dispositivo d
                        ON se.id_dispositivo = d.id_dispositivo
                      WHERE a.id_alerta = %s
                        AND d.id_salon = s.id_salon
                        AND a.estado = TRUE
                  )
              )
            RETURNING *
        """, (
            datos.id_alerta,
            datos.codigo,
            datos.tipo_accion,
            datos.modo,
            datos.fecha_accion,
            datos.observacion,
            datos.id_salon,
            datos.id_alerta,
            datos.id_alerta
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


def obtener_accion_por_id(id_accion):
    conexion = Database().get_connection()

    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT *
            FROM accion_ventilacion
            WHERE id_accion = %s
              AND estado = TRUE
        """, (id_accion,))

        return convertir_diccionario(
            cursor, cursor.fetchone()
        )

    finally:
        conexion.close()


def actualizar_accion(id_accion, datos):
    conexion = Database().get_connection()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            UPDATE accion_ventilacion
            SET id_salon = %s,
                id_alerta = %s,
                codigo = %s,
                tipo_accion = %s,
                modo = %s,
                fecha_accion = COALESCE(
                    %s, fecha_accion
                ),
                observacion = %s
            WHERE id_accion = %s
              AND estado = TRUE
              AND EXISTS (
                  SELECT 1
                  FROM salon s
                  WHERE s.id_salon = %s
                    AND s.estado = TRUE
                    AND (
                        %s IS NULL
                        OR EXISTS (
                            SELECT 1
                            FROM alerta a
                            JOIN medicion m
                              ON a.id_medicion = m.id_medicion
                            JOIN sensor se
                              ON m.id_sensor = se.id_sensor
                            JOIN dispositivo d
                              ON se.id_dispositivo = d.id_dispositivo
                            WHERE a.id_alerta = %s
                              AND d.id_salon = s.id_salon
                              AND a.estado = TRUE
                        )
                    )
              )
            RETURNING *
        """, (
            datos.id_salon,
            datos.id_alerta,
            datos.codigo,
            datos.tipo_accion,
            datos.modo,
            datos.fecha_accion,
            datos.observacion,
            id_accion,
            datos.id_salon,
            datos.id_alerta,
            datos.id_alerta
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


def desactivar_accion(id_accion):
    conexion = Database().get_connection()

    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE accion_ventilacion
            SET estado = FALSE
            WHERE id_accion = %s
              AND estado = TRUE
            RETURNING id_accion
        """, (id_accion,))

        resultado = cursor.fetchone()
        conexion.commit()

        return resultado is not None

    except Exception:
        conexion.rollback()
        raise

    finally:
        conexion.close()
