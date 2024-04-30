
import os

from dotenv import load_dotenv

load_dotenv()

OLLAMA_PROXY_URL = os.getenv("OLLAMA_PROXY_URL")
