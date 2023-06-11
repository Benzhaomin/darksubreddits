import json

with open("subreddits.json", "r") as f:
    subreddits = json.load(f)

total = len(subreddits)
private = sum(subreddits.values())
public =  total - private

print(f"{private}/{total}")
