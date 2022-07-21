import pytest
import starlette.status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path

from api.db import Base, get_db
from api.main import app

ASYNC_DB_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture
async def async_client():
    # Async用のengineとsessionを作成
    async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
    async_session = sessionmaker(
        autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
    )

    # テスト用にオンメモリのSQLiteテーブルを初期化（関数ごとにリセット）
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # DIを使ってFastAPIのDBの向き先をテスト用DBに変更
    async def get_test_db():
        async with async_session() as session:
            yield session

    app.dependency_overrides[get_db] = get_test_db

    # テスト用に非同期HTTPクライアントを返却
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


"""
About assert
FYI:
https://codezine.jp/article/detail/12179
"""

@pytest.mark.asyncio
async def test_upload_and_read(async_client):
    fpath = Path("handwriting_pics/0.jpg")
    with open(fpath, "rb") as f:
        response = await async_client.post("/images", files={"files": ("0.jpg", f, "image/jpeg")})
        assert response.status_code == starlette.status.HTTP_200_OK
        response_obj = response.json()
        assert "file_id" in response_obj

    response = await async_client.get("/images")
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert len(response_obj) == 1
    assert "file_id" in response_obj[0]
    assert response_obj[0]["filename"] == "0.jpg"


@pytest.mark.asyncio
async def test_prediction_image(async_client):
    fpath = Path("handwriting_pics/0.jpg")
    with open(fpath, "rb") as f:
        response = await async_client.post("/images", files={"files": ("0.jpg", f, "image/jpeg")})
        assert response.status_code == starlette.status.HTTP_200_OK
        response_obj = response.json()
        assert "file_id" in response_obj
        file_id = response_obj["file_id"]
    
    # TODO: DI (change file storage from present S3 to test storage)
    response = await async_client.post("/probabilities/"+file_id)
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["file_id"] == file_id
    assert ("observed_result", "predicted_result", "accuracy") in response_obj
