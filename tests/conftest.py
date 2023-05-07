from collections.abc import AsyncGenerator
from src.main import init_app
from src.config import get_config, Config
from src.redis import RedisStorage
from redis.asyncio import Redis
from aiohttp import web
import pytest


@pytest.fixture
def env_config() -> Config:
    return get_config()


@pytest.fixture
def app(env_config) -> web.Application:
    app = init_app(env_config)
    return app


@pytest.fixture
async def client(aiohttp_client, app):
    client = await aiohttp_client(app)
    return client


@pytest.fixture()
async def redis_storage(env_config: Config) -> AsyncGenerator:
    redis = Redis(
        host=env_config.REDIS_HOST,
        port=int(env_config.REDIS_PORT),
        password=env_config.REDIS_PASSWORD.get_secret_value(),
        decode_responses=True,
    )
    await redis.ping()
    redis_storage = RedisStorage(redis)
    try:
        yield redis_storage
    finally:
        await redis.flushdb()
        await redis.close()


@pytest.fixture
def currency_rates():
    return [
        ("USD/RUR", 42),
        ("USD/EUR", 42),
        ("USD/UAH", 42),
        ("USD/KZT", 42),
        ("USD/AFN", 42),
        ("RUR/AFN", 420),
        ("RUR/UAH", 69),
        ("KZT/UAH", 42069),
    ]
