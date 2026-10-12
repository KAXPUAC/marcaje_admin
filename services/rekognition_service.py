from core.aws import aws_client


class RekognitionService:

    @staticmethod
    def obtener_nombre_coleccion(departamento_id: str) -> str:
        # Formato estándar de colección: ej. "depto_contabilidad"
        return f"depto_{departamento_id.lower().strip()}"

    @classmethod
    def buscar_rostro_en_departamento(cls, departamento_id: str, image_bytes: bytes, umbral: float = 90.0):
        collection_id = cls.obtener_nombre_coleccion(departamento_id)

        # Búsqueda optimizada únicamente dentro de la colección del departamento
        response = aws_client.rekognition.search_faces_by_image(
            CollectionId=collection_id,
            Image={'Bytes': image_bytes},
            FaceMatchThreshold=umbral,
            MaxFaces=1
        )

        matches = response.get('FaceMatches', [])
        if not matches:
            return None

        return {
            "face_id": matches[0]['Face']['FaceId'],
            "similarity": matches[0]['Similarity']
        }
