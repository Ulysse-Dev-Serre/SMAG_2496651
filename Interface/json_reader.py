import json

def get_json(f):
    with open(f,"r") as file:
        data = json.load(file)
        return len(data["alerts_by_time"])