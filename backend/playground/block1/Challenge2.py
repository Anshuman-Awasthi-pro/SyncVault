massive_commit = {
    "repo": "SyncVault-Core",
    "files": ["index.html", "style.css", "main.py", "redis_client.py", "ai_scanner.py", "database.py"]
}

# Write your code below this line:
file = massive_commit["files"]
files_to_scan = file[:-4:-1]
print(files_to_scan)