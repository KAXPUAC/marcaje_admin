from pydantic import BaseModel
from typing import Optional

class CreateSessionResponse(BaseModel):
    session_id: str

class VerifyLivenessRequest(BaseModel):
    session_id: str
    departamento_id: str
    tipo_marcaje: str  # 'ENTRADA', 'SALIDA', etc.

class MarcajeResponse(BaseModel):
    status: str
    mensaje: str
    empleado_id: int
    similitud: float