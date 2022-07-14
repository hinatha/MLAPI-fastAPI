import pickle
from sqlalchemy.ext.asyncio import AsyncSession

import numpy as np

import api.preparations.image as image_preparation
import api.schemas.image as image_schema
import api.schemas.ml as ml_schema

from .preprocess import get_shrinked_img


async def evaluate_probs(file_id: image_schema.FileIdModel, db: AsyncSession) -> ml_schema.PredictResult:
    """テストデータを利用してロジスティック回帰の学習済みモデルのアウトプットを評価"""
    filenames = await(image_preparation.extract_filenames(file_id, db))
    img_test = get_shrinked_img(filenames)

    with open("/src/api/predictions/model.pickle", mode="rb") as fp:
        model = pickle.load(fp)

    X_true = [int(filename[:1]) for filename in filenames]
    X_true = np.array(X_true)

    predicted_result = model.predict(img_test).tolist()
    accuracy = model.score(img_test, X_true).tolist()
    observed_result = X_true.tolist()

    predict = {
                "file_id": file_id,
                "observed_result": observed_result,
                "predicted_result": predicted_result,
                "accuracy": accuracy,
            }


    return predict