from typing import BinaryIO

from minio import Minio

from src.app.core.config import settings

_client = Minio(
    settings.S3_ENDPOINT_URL.replace("http://", "").replace("https://", ""),
    access_key=settings.S3_ACCESS_KEY,
    secret_key=settings.S3_SECRET_KEY,
    secure=settings.S3_ENDPOINT_URL.startswith("https"),
)


def ensure_bucket_exists() -> None:
    found = _client.bucket_exists(settings.S3_BUCKET_NAME)
    if not found:
        _client.make_bucket(settings.S3_BUCKET_NAME)


def upload_image(file_obj: BinaryIO, filename: str, content_type: str) -> str:
    ensure_bucket_exists()
    _client.put_object(
        bucket_name=settings.S3_BUCKET_NAME,
        object_name=filename,
        data=file_obj,
        length=-1,
        part_size=10 * 1024 * 1024,
        content_type=content_type,
    )

    return f"{settings.S3_ENDPOINT_URL}/{settings.S3_BUCKET_NAME}/{filename}"
