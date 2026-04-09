import os
import redis.asyncio as redis
import asyncio
import json
from dotenv import load_dotenv

load_dotenv()
REDIS_URL = os.getenv("REDIS_URL")

redis_db = redis.from_url(REDIS_URL, decode_responses = True)

async def start_worker():
    #we want this loop to always work even if bin is empty
    while(True):
        #rpop remove file from right of bin and b block or hold cpu when bin is empty
        result = await redis_db.brpop("code_pipeline")
        
        #o index shows name of bin and 1st index
        raw_string = result[1]
        job_data = json.loads(raw_string)
        
        #result stored tuple containing name file name etc.
        # print(f"Successfully executed!!: {result}")
        print(f"Chef received {job_data['filename']} from {job_data['user']}!")

#this line runs the async function it act as key(event loop) which runs the coroutine b=object which is stored in memeory we don't need this code in previous redis code as there uvicorn act as event loop executor and worker is completely disconnected from Uvicorn and FastAPI. It is a standalone, raw Python script         
asyncio.run(start_worker())
#is there a way to test my current code if it works perfectly or not like running it or something like that