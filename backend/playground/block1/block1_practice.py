# Checking for the python basic like list, loop, dict, list comprehension
files = ["main.py", "database.js", "config.yaml", "secret.txt"]
python_files = [f for f in files if f.endswith(".py")]
 
report = {
    'status' : "scanning",
    'found_files' : python_files,
    "count": len(python_files)
}

for l in files:
    print(f"Scanning {l}...")
    
# python functions and any keyword
threats = ["password","api", "api_key"]

def analyze_code(file_name : str, content : str) -> dict:
    content_lower = content.lower()
    is_vulnerable = any(word in content_lower for word in threats)    
    
    return {
        "file" : file_name,
        "result" : "VULNERABLE" if is_vulnerable else "CLEAN"
    }
#