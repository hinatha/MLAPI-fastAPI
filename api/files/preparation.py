import uuid
import boto3
from fastapi import UploadFile, Depends

from functools import lru_cache
from werkzeug.utils import secure_filename

from sqlalchemy.ext.asyncio import AsyncSession

from api import config
from api.models.image import ImageInfo
from api.schemas.image import FileIdModel


@lru_cache()
def get_settings():
    return config.Settings()

async def insert_filedata(
    files: list[UploadFile], db: AsyncSession
) -> FileIdModel:
    """手書き文字画像のファイル名をデータベースに保存し、ファイルをS3のフォルダにアップロードする"""
    file_id = str(uuid.uuid4())

    settings = get_settings()

    s3_client = boto3.client("s3")
    bucket_name = settings.bucket_name
    dir_name = settings.folder_name
    region = settings.aws_default_region

    # Execute make bucket
    try:
        s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': region
            }
        )
    except:
        pass

    # Execute files upload to S3
    for file in files:
        filename = secure_filename(file.filename)
        image_info = ImageInfo(file_id=file_id, filename=filename)
        db.add(image_info)
        key = dir_name + filename
        s3_client.put_object(Body=file.file, Bucket=bucket_name, Key=key)

    await db.commit()
    file_id_json = {"file_id": file_id}
    return file_id_json
