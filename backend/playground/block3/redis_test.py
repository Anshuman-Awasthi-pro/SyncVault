import redis.asyncio as redis
import asyncio
import json
import dotenv

REDIS_URL = "rediss://fake-secure-url.upstash.io:30000"
async def emergency_backup(payload : dict):
    r = redis.from_url(REDIS_URL, decode_responses = True)
    await r.lpush("quarantine_zone", json.dumps(payload))
    print(f"Quarantine Zone Currently hold {r.llen("quarantine_zone")}")