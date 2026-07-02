from fastapi import FastAPI
from pydantic import BaseModel
from backend.services.redis_client import push_batch_to_queue

app = FastAPI()

class CommitPayload(BaseModel): #inhertiting from BaseModel to create a model for the payload
    user : str
    filename : str
    code : str

@app.get("/health")
def health():
    return {"project" : "SyncVault", "status" : "Active and Listening"}

@app.post("/api/push")
async def receive_code(payload : list[CommitPayload]):
    await push_batch_to_queue("code_pipeline",payload)
    return {"status" : "queued"}

