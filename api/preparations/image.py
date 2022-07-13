import uuid
import boto3
from fastapi import UploadFile, Depends
from typing import List

from functools import lru_cache
from werkzeug.utils import secure_filename

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result

from api import config
import api.models.image as image_model
import api.schemas.image as image_schema


# Return all image info
async def get_images(db: AsyncSession) -> List[image_schema.ImageList]:
    result: Result = await (
        db.execute(
            select(
                image_model.ImageInfo.file_id,
                image_model.ImageInfo.filename,
            )
        )
    )
    return result.all()


# Setting S3 info
@lru_cache()
def get_settings():
    return config.Settings()


# Post image file, file name as metadata and return file_id
async def insert_filedata(files: list[UploadFile], db: AsyncSession) -> image_schema.FileIdModel:
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
        image_info = image_model.ImageInfo(file_id=file_id, filename=filename)
        db.add(image_info)
        key = dir_name + filename
        s3_client.put_object(Body=file.file, Bucket=bucket_name, Key=key)

    await db.commit()

    file_id_json = {"file_id": file_id}
    return file_id_json
