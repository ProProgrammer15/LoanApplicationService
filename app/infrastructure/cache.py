import redis.asyncio as redis
import os

REDIS_URL = os.getenv("REDIS_URL")

redis_client = redis.Redis.from_url(REDIS_URL)


async def cache_status_in_redis(applicant_id: str, status: str):
    """
    Cache loan application status in Redis
    :param applicant_id:
    :param status:
    :return: None
    """
    await redis_client.setex(applicant_id, 3600, status)  # 1 hour TTL


