from fastapi import APIRouter, HTTPException
from core.aws import aws_client
from schemas.liveness import CreateSessionResponse, VerifyLivenessRequest, MarcajeResponse
from services.rekognition_service import RekognitionService
from repositories.marcaje_repo import MarcajeRepository

router = APIRouter()


@router.post("/create-session", response_model=CreateSessionResponse)
def crear_sesion_liveness():
    """Inicia la sesión de prueba de vida (Face Liveness) en AWS."""
    try:
        response = aws_client.rekognition.create_face_liveness_session()
        return {"session_id": response['SessionId']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear sesión AWS: {str(e)}")


@router.post("/verify", response_model=MarcajeResponse)
def verificar_liveness_y_marcar(payload: VerifyLivenessRequest):
    """Verifica Liveness, busca el rostro en el grupo/departamento e inserta en Oracle 12c."""

    # 1. Obtener resultado de la prueba de vida de AWS
    result = aws_client.rekognition.get_face_liveness_session_results(
        SessionId=payload.session_id
    )

    if result.get('Status') != 'SUCCEEDED' or result.get('Confidence', 0) < 85.0:
        raise HTTPException(status_code=400, detail="Prueba de vida fallida o posible fraude.")

    # 2. Extraer frame de alta referencia
    reference_bytes = result['ReferenceImage']['Bytes']

    # 3. Buscar rostro solo dentro de la colección del departamento
    coincidencia = RekognitionService.buscar_rostro_en_departamento(
        departamento_id=payload.departamento_id,
        image_bytes=reference_bytes
    )

    if not coincidencia:
        raise HTTPException(status_code=404, detail="Empleado no reconocido en este departamento.")

    # 4. Obtener ID de empleado vinculado en Oracle 12c
    empleado_id = MarcajeRepository.obtener_empleado_por_face_id(coincidencia['face_id'])
    if not empleado_id:
        raise HTTPException(status_code=404, detail="El rostro no está vinculado a ningún empleado activo.")

    # 5. Insertar marcaje en Oracle 12c
    MarcajeRepository.insertar_marcaje(
        empleado_id=empleado_id,
        tipo_marcaje=payload.tipo_marcaje,
        similitud=coincidencia['similarity']
    )

    return {
        "status": "SUCCESS",
        "mensaje": "Marcaje registrado correctamente",
        "empleado_id": empleado_id,
        "similitud": coincidencia['similarity']
    }
