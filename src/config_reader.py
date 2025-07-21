import json

def load_config(path="config/config.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_openai_key():
    return load_config()["openai_api_key"]
