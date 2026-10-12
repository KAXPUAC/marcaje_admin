import boto3
from core.config import settings


class AWSClient:
    def __init__(self):
        self.rekognition = boto3.client(
            'rekognition',
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            aws_bucket_name=settings.AWS_BUCKET_NAME,
        )


aws_client = AWSClient()
