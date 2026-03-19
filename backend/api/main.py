from fastapi import FastAPI
from backend.services.redis_client import push_batch_to_queue

app = FastAPI()

@app.get("/health")
def health():
    return {"project" : "SyncVault", "status" : "Active and Listening"}

@app.post("/api/push")
async def receive_code(payload : list[dict]):
    await push_batch_to_queue("code_pipeline",payload)
    return {"status" : "queued"}