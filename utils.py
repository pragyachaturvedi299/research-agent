import os
import time
import yaml
from dotenv import load_dotenv
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

load_dotenv()
api_key = os.getenv("OPEN_API_KEY")

# Load local model if API key is not available or expired
model_dir = os.path.join(os.path.dirname(__file__), "model")
if os.path.exists(model_dir):
    print("Loading local Phi-2 model...")
    tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(model_dir, trust_remote_code=True)
    # Set pad token if not set
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    generator = pipeline("text-generation", model=model, tokenizer=tokenizer, device=-1)  # CPU
    client = None
else:
    from openai import OpenAI
    if not api_key:
        raise ValueError("OPENAI_API_KEY missing in .env")
    client = OpenAI(api_key=api_key)
    generator = None

def load_config(path="config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def measure_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        out = func(*args, **kwargs)
        return out, time.time() - start
    return wrapper
