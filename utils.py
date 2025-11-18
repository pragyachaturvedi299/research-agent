import os
import time
import yaml
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPEN_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY missing in .env")

client = OpenAI(api_key=api_key)

def load_config(path="config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def measure_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        out = func(*args, **kwargs)
        return out, time.time() - start
    return wrapper
