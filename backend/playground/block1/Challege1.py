recent_pushes = [
    {"commit_id": "a1b2", "user": "anshuman", "status": "scanned_clean"},
    {"commit_id": "c3d4", "user": "peer_1", "status": "pending"},
    {"commit_id": "e5f6", "user": "peer_2", "status": "scanned_malicious"},
    {"commit_id": "g7h8", "user": "anshuman", "status": "pending"}
]

# Write your code below this line:
action_required = [push["commit_id"] for push in recent_pushes if push["status"] == "pending"]
# for push in recent_pushes:
#     if push["status"] == "pending":
#         action_required.append(push["commit_id"])
print(action_required)