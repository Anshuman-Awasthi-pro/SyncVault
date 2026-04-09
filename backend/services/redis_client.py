import os
import redis.asyncio as redis
import json
from dotenv import load_dotenv

load_dotenv()
REDIS_URL = os.getenv("REDIS_URL")

#when we store data in database it converts it into bytes so we use decode_response to decode the incoming data
redis_db = redis.from_url(REDIS_URL, decode_responses = True, ssl_cert_reqs="none")   

#queue_name is the name of bin and can be change according to our needs{code_pipeline,quarantine_zone}
#payload is the files pushed by user
async def push_batch_to_queue(queue_name : str, payload : list):
    
    #Transaction as true works as donot distrub sign and avoid the server merging the files of different user pushed in same milisecond
    async with redis_db.pipeline(transaction=True) as pipe:     
        for file in payload:
            pipe.lpush(queue_name, json.dumps(file))
        await  pipe.execute()
        print(f"Success!! File {len(payload)} Pushed")
        
        
# Challanges faced {
#     1>figuring out SSL connection strings for a pipelined message broker. The connection was not establishing and the reason   for that is extra 's' in redis (rediss) in .env
        
# }