import os
import json

def load_config():
    if os.path.exists("config/config.json"):
        with open("config/config.json", "r") as f:
            return json.load(f)
    return {}

def get_openai_key():
    # ✅ Look for env variable first
    return os.environ.get("OPENAI_API_KEY") or load_config().get("openai_api_key")
