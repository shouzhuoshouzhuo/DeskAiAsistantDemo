import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

API_KEY = os.getenv("API_KEY")
MODEL = os.getenv("MODEL", "deepseek-v3.2")
BASE_URL = os.getenv("BASE_URL", "https://4sapi.com/v1")