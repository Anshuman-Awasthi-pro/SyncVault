import json

Threats = ["password","api","api_key","secret_key"]
async def SyncVault_scanner(incoming_data : dict):
    content = incoming_data["code"].lower()
    is_unsafe = any(word in content for word in Threats)
    result = {
        "file_name" : incoming_data["filename"],
        "is_dangerous" : True if is_unsafe else False
    }
    return json.dumps(result)

def frontend_request_filter(incoming_data: dict):
    Crucial = ["filename", "code"]
    for key in Crucial :
        if key not in incoming_data :
            return {"error": "Missing required fields", "status": 400}