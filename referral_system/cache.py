import redis.asyncio as redis
import json


redis_client = redis.from_url("redis://localhost", decode_responses=True)


async def cache_referral_code(code: str, data: dict, ttl: int = 3600):
    data_str = json.dumps(data)
    await redis_client.set(code, data_str, ex=ttl)


async def get_cached_referral_code(code: str):
    return await redis_client.get(code)
