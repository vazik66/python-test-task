import typing as tp
from abc import ABC, abstractmethod
from logging import getLogger

from aiohttp import web

from redis.asyncio import Redis

log = getLogger(__name__)


async def setup_redis(app: web.Application) -> tp.AsyncGenerator:
    cfg = app["cfg"]
    log.info("Connecting to redis")
    app["storage"] = Redis(
        host=cfg.REDIS_HOST,
        port=int(cfg.REDIS_PORT),
        password=cfg.REDIS_PASSWORD.get_secret_value(),
        decode_responses=True,
    )

    await app["storage"].ping()
    log.info("Redis connected")

    try:
        yield
    finally:
        await app["storage"].close()
        log.info("Connection to redis closed")


class Storage(ABC):
    @abstractmethod
    async def flush(self) -> bool:
        ...

    @abstractmethod
    async def bulk_set(self, data: list[tuple[str, str]]) -> tp.NoReturn:
        ...

    @abstractmethod
    async def get(self, key: str) -> str | None:
        ...


class StorageInMemory(Storage):
    data: dict = {}

    async def flush(self) -> bool:
        self.data.clear()
        return True

    async def bulk_set(self, data: list[tuple[str, str]]) -> tp.NoReturn:
        for key, value in data:
            self.data[key] = value

    async def get(self, key: str) -> str | None:
        return self.data.get(key)


class RedisStorage(Storage):
    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    async def flush(self) -> bool:
        return await self.redis.flushdb(asynchronous=True)

    async def bulk_set(self, data: list[tuple[str, str]]) -> tp.NoReturn:
        pipeline = self.redis.pipeline()
        for key, value in data:
            pipeline.set(name=key, value=value)

        resp = await pipeline.execute()
        if not all(resp):
            log.debug(resp)
            log.warn("Not all data is saved")

    async def get(self, key: str) -> str | None:
        return await self.redis.get(key)
