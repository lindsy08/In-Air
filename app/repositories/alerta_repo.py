
from app.core.database import Database


def convertir_diccionario(cursor, fila):
    if fila is None:
        return None

    columnas = [col[0] for col in cursor.description]
    return dict(zip(columnas, fila))


def listar_alertas():
    conexion = Database().get_connection()

    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT a.*,
                   m.valor AS valor_medicion,
                   m.fecha_medicion,
                   t.nombre AS tipo_sensor,
                   t.unidad_medida,
                   s.codigo AS codigo_salon,
                   u.valor_minimo,
                   u.valor_maximo
            FROM alerta a
            JOIN medicion m
                ON a.id_medicion = m.id_medicion
            JOIN sensor se
                ON m.id_sensor = se.id_sensor
            JOIN tipo_sensor t
                ON se.id_tipo_sensor = t.id_tipo_sensor
            JOIN dispositivo d
                ON se.id_dispositivo = d.id_dispositivo
            JOIN salon s
                ON d.id_salon = s.id_salon
            JOIN umbral u
                ON a.id_umbral = u.id_umbral
            WHERE a.estado = TRUE
            ORDER BY a.fecha_alerta DESC, a.id_alerta DESC
        """)

        columnas = [col[0] for col in cursor.description]

        return [
            dict(zip(columnas, fila))
            for fila in cursor.fetchall()
        ]

    finally:
        conexion.close()


def crear_alerta(datos):
    conexion = Database().get_connection()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO alerta (
                id_medicion,
                id_umbral,
                nivel,
                mensaje,
                fecha_alerta,
                atendida
            )
            SELECT m.id_medicion,
                   u.id_umbral,
                   %s, %s,
                   COALESCE(%s, CURRENT_TIMESTAMP),
                   %s
            FROM medicion m
            JOIN sensor se
                ON m.id_sensor = se.id_sensor
            JOIN dispositivo d
                ON se.id_dispositivo = d.id_dispositivo
            JOIN umbral u
                ON u.id_tipo_sensor = se.id_tipo_sensor
               AND u.id_salon = d.id_salon
            WHERE m.id_medicion = %s
              AND u.id_umbral = %s
              AND m.estado = TRUE
              AND se.estado = TRUE
              AND d.estado = TRUE
              AND u.estado = TRUE
              AND (
                  m.valor < u.valor_minimo
                  OR m.valor > u.valor_maximo
              )
            RETURNING *
        """, (
            datos.nivel,
            datos.mensaje,
            datos.fecha_alerta,
            datos.atendida,
            datos.id_medicion,
            datos.id_umbral
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


def obtener_alerta_por_id(id_alerta):
    conexion = Database().get_connection()

    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT *
            FROM alerta
            WHERE id_alerta = %s
              AND estado = TRUE
        """, (id_alerta,))

        return convertir_diccionario(
            cursor, cursor.fetchone()
        )

    finally:
        conexion.close()


def actualizar_alerta(id_alerta, datos):
    conexion = Database().get_connection()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            UPDATE alerta
            SET id_medicion = %s,
                id_umbral = %s,
                nivel = %s,
                mensaje = %s,
                fecha_alerta = COALESCE(
                    %s, fecha_alerta
                ),
                atendida = %s
            WHERE id_alerta = %s
              AND estado = TRUE
              AND EXISTS (
                  SELECT 1
                  FROM medicion m
                  JOIN sensor se
                    ON m.id_sensor = se.id_sensor
                  JOIN dispositivo d
                    ON se.id_dispositivo = d.id_dispositivo
                  JOIN umbral u
                    ON u.id_tipo_sensor = se.id_tipo_sensor
                   AND u.id_salon = d.id_salon
                  WHERE m.id_medicion = %s
                    AND u.id_umbral = %s
                    AND m.estado = TRUE
                    AND se.estado = TRUE
                    AND d.estado = TRUE
                    AND u.estado = TRUE
                    AND (
                        m.valor < u.valor_minimo
                        OR m.valor > u.valor_maximo
                    )
              )
            RETURNING *
        """, (
            datos.id_medicion,
            datos.id_umbral,
            datos.nivel,
            datos.mensaje,
            datos.fecha_alerta,
            datos.atendida,
            id_alerta,
            datos.id_medicion,
            datos.id_umbral
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


def desactivar_alerta(id_alerta):
    conexion = Database().get_connection()

    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE alerta
            SET estado = FALSE
            WHERE id_alerta = %s
              AND estado = TRUE
            RETURNING id_alerta
        """, (id_alerta,))

        resultado = cursor.fetchone()
        conexion.commit()

        return resultado is not None

    except Exception:
        conexion.rollback()
        raise

    finally:
        conexion.close()
