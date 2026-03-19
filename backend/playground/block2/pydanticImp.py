from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class CodeFile(BaseModel):
    file_name : str
    source_code : str

class SyncVaultCommit(BaseModel):
    commit_id : str
    files : List[CodeFile]
    
@app.post("/ingest_commit")
async def accept(payload : SyncVaultCommit): #cyrrently payload is object
    pending_files = [name.file_name for name in payload.files]
    # payload_dict = payload.model_dump()     model_dump convert it into dictionary
    for name in payload.files:
        print(name.source_code)
    return {"status": "Commit received", "commit": payload.commit_id, "files_to_scan": pending_files}