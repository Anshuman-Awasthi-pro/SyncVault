from dotenv import load_dotenv
import os
import redis.asyncio as redis
from fastapi import FastAPI
import json

#challenge 1
load_dotenv()
REDIS_KEY = os.getenv("REDIS_URL")

#challlenge 2
app = FastAPI()
@app.post("/api/lockdown")
def fun(files : dict):
    #i don't know what do you mean when you say return the route
    return {"status" : "Success"}

#challenge 3 well i am not quite remembering how to traverse dictionary
redis_db = redis.from_url(REDIS_KEY, decode_responses = True)
async def redis_fun(files : dict):
    async with redis_db.pipeline(transaction=True) as pipe:
        for file in files:
            pipe.lpush("lockdown_zone",json.dumps(file))
        await pipe.execute()
        print(f"Files Submitted Successfully")
        
#also i can't remember it all so i take help from my previous code to jog off my memories
