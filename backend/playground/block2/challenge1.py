from fastapi import FastAPI
app = FastAPI()

@app.get("/health")
async def check_health():
    return {"project": "SyncVault", "status": "Active and Listening"}

@app.post("/api/push")
async def receive_code(payload : dict):
    print("Received new push from user!")
    return {"message": "Code push received safely", "queued": True}