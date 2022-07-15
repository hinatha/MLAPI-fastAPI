import numpy as np
from PIL import Image
from io import BytesIO
import boto3
from typing import List

from api.config import get_settings
import api.schemas.ml as ml_schema
import api.schemas.image as image_schema


def get_grayscale(filenames: List[image_schema.FileNameModel]) -> bytes:
    """読み込んだ手書き文字画像の色をグレースケールに変換する関数 (グレースケールは色の濃淡の明暗を分ける技法のことです。)"""
    settings = get_settings()
    s3_client = boto3.client("s3")
    bucket_name = settings.bucket_name
    dir_name = settings.folder_name
    for filename in filenames:
        key = dir_name + filename
        img_file = s3_client.get_object(Bucket=bucket_name, Key=key)['Body'].read()
        img = Image.open(BytesIO(img_file)).convert("L")
        yield img


def shrink_image(
    img, offset=5, crop_size: int = 8, pixel_size: int = 255, max_size: int = 16
):
    """画像サイズを8x8ピクセルのサイズに統一し、明るさも16階調のグレイスケールで白黒に変換する関数"""
    img_array = np.asarray(img)
    h_indxis = np.where(img_array.min(axis=0) < 255)
    v_indxis = np.where(img_array.min(axis=1) < 255)
    h_min, h_max = h_indxis[0].min(), h_indxis[0].max()
    v_min, v_max = v_indxis[0].min(), v_indxis[0].max()
    width, hight = h_max - h_min, v_max - v_min

    if width > hight:
        center = (v_max + v_min) // 2
        left = h_min - offset
        upper = (center - width // 2) - 1 - offset
        right = h_max + offset
        lower = (center + width // 2) + offset
    else:
        center = (h_max + h_min + 1) // 2
        left = (center - hight // 2) - 1 - offset
        upper = v_min - offset
        right = (center + hight // 2) + offset
        lower = v_max + offset

    img_croped = img.crop((left, upper, right, lower)).resize((crop_size, crop_size))
    img_data256 = pixel_size - np.asarray(img_croped)

    min_bright, max_bright = img_data256.min(), img_data256.max()
    img_data16 = (img_data256 - min_bright) / (max_bright - min_bright) * max_size
    return img_data16


def get_shrinked_img(filenames: List[image_schema.FileNameModel]) -> List[int]:
    """モデルにインプットする画像の数値データのリストを作成する関数"""
    img_test = np.empty((0, 64))
    for img in get_grayscale(filenames):
        img_data16 = shrink_image(img)
        img_test = np.r_[img_test, img_data16.astype(np.uint8).reshape(1, -1)]
    return img_test
