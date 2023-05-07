from src.redis import StorageInMemory, RedisStorage
from src.converter.service import ConvertService


async def test_convertaion():
    convert_service = ConvertService(StorageInMemory())
    converted = convert_service._convert(53, 26.531231)
    assert converted == 1406.16


async def test_redis_set_bulk(redis_storage: RedisStorage, currency_rates):
    await redis_storage.bulk_set(currency_rates)
    res = await redis_storage.redis.get(currency_rates[0][0])
    assert float(res) == currency_rates[0][1]


async def test_redis_get(redis_storage: RedisStorage, currency_rates):
    await redis_storage.bulk_set(currency_rates)
    res = await redis_storage.get(currency_rates[0][0])
    assert float(res) == currency_rates[0][1]


async def test_convert_valid(client):
    resp = await client.post(
        "/database?merge=1", json={"pairs": [{"currency_pair": "USD/RUR", "rate": 42}]}
    )
    assert resp.status == 200

    resp = await client.get("/convert?from=USD&to=RUR&amount=42")
    assert resp.status == 200
    assert (await resp.json())["result"] == 1764.0


async def test_update_merge_0_valid(client):
    resp = await client.post("/database?merge=0")
    assert resp.status == 200

    resp = await client.get("/convert?from=USD&to=RUR&amount=100")
    assert (await resp.json())["result"] == -1


async def test_post_invalid_json(client):
    resp = await client.post("/database?merge=1", data='{"asd": ')
    assert resp.status == 422


async def test_post_invalid_model(client):
    resp = await client.post(
        "/database?merge=1",
        json={"pairs": [{"currency_pair": "LKJH/LKJH", "rate": -5}]},
    )
    assert resp.status == 422


async def test_update_with_nothing(client):
    resp = await client.post(
        "/database",
    )
    assert resp.status == 422
