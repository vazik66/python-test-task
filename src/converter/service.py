from logging import getLogger
from aiohttp import web

from src.converter.models import ConvertCurrecnyQuery, UpdateRatesBody, UpdateRatesQuery
from src.redis import Storage, RedisStorage

log = getLogger(__name__)


class ConvertService:
    def __init__(self, storage: Storage):
        self.storage = storage

    async def update(self, params: UpdateRatesQuery, data: UpdateRatesBody | None):
        if params.merge and not data:
            raise Exception("When merge=1, body must be provided")

        if not params.merge:
            await self.storage.flush()
            return

        data = [(pair.currency_pair, str(pair.rate)) for pair in data.pairs]
        await self.storage.bulk_set(data)

    async def convert_currency(self, convert: ConvertCurrecnyQuery) -> float:
        key = f"{convert.from_}/{convert.to}"
        rate = await self.storage.get(key)
        log.debug(f"{key= } {rate=}")
        if rate:
            return self._convert(convert.amount, float(rate))

        key = f"{convert.to}/{convert.from_}"
        rate = await self.storage.get(key)
        log.debug(f"reversed {key= } {rate=}")
        if not rate:
            return -1
        return self._convert(convert.amount, 1 / float(rate))

    def _convert(self, amount: float, rate: float) -> float:
        return round(amount * float(rate), 2)


async def init_service(app: web.Application):
    app["convert_service"] = ConvertService(RedisStorage(app["storage"]))
    yield
