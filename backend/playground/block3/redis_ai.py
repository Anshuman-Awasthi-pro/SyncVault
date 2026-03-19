import redis.asyncio as redis
import json
import dotenv

REDIS_URL = ""

r = redis.from_url(REDIS_URL, decoded_responses = True)  
    
async def push_to_queue(files: list, repo_name: str):
    if len(files) > 1:
        async with r.pipeline(transaction=True) as pipe: # Boolean True
            for name in files:
                push = {
                    "filename": name,
                    "reponame": repo_name,
                    "status": "pending"
                }
                # Call lpush on 'pipe', not 'r'
                await pipe.lpush("repo_task", json.dumps(push))
            await pipe.execute() # Call execute on 'pipe'
            print(f"Batch of {len(files)} pushed.")
            
    elif len(files) == 1:
        push = {
            "filename": files[0],
            "reponame": repo_name,
            "status": "pending"
        }
        # Direct push using 'r'
        await r.lpush("repo_task", json.dumps(push))
        print(f"Single file {files[0]} pushed.")