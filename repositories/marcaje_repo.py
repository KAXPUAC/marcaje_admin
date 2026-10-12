import oracledb
from core.database import get_connection


class MarcajeRepository:

    @staticmethod
    def obtener_empleado_por_face_id(face_id: str) -> int:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            sql = "SELECT EMPLEADO_ID FROM EMPLEADO_BIOMETRIA WHERE FACE_ID = :1"
            cursor.execute(sql, [face_id])
            row = cursor.fetchone()
            return row[0] if row else None
        finally:
            conn.release(cursor)

    @staticmethod
    def insertar_marcaje(empleado_id: int, tipo_marcaje: str, similitud: float) -> int:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            # Retorna el ID generado por IDENTITY en Oracle 12c
            out_id = cursor.var(oracledb.NUMBER)
            sql = """
                  INSERT INTO MARCAJES_ASISTENCIA
                      (EMPLEADO_ID, TIPO_MARCAJE, SIMILITUD_PORCENTAJE)
                  VALUES (:1, :2, :3) RETURNING MARCAJE_ID
                  INTO :4 \
                  """
            cursor.execute(sql, [empleado_id, tipo_marcaje, similitud, out_id])
            conn.commit()
            return int(out_id.getvalue()[0])
        finally:
            conn.release(cursor)
