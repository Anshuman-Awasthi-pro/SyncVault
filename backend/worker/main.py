import os
import redis.asyncio as redis
import asyncio
import json
from dotenv import load_dotenv
from ai_scanner import check_if_safe

load_dotenv()
REDIS_URL = os.getenv("REDIS_URL")

redis_db = redis.from_url(REDIS_URL, decode_responses = True)

async def start_worker():
    #we want this loop to always work even if bin is empty
    while(True):
        #rpop remove file from right of bin and b block or hold cpu when bin is empty
        result = await redis_db.brpop("code_pipeline")
        
        #0 index shows name of bin and 1 index shows the file name
        raw_string = result[1]
        job_data = json.loads(raw_string) 
        
        #result stored tuple containing name file name etc.
        # print(f"Successfully executed!!: {result}")
        print(f"Chef received {job_data['filename']} from {job_data['user']}!")
        
        if check_if_safe(job_data['code']):
            print(f"✅ AI Scan Passed: {job_data['filename']} is clean.")
        else:
            print(f"❌ AI Scan Failed: {job_data['filename']} contains potentially harmful code.")
        
        
        
            

#this line is used to create the multilane high way for async function, it starts the engine(event loop)      
asyncio.run(start_worker())
