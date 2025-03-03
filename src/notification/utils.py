import os

import requests
from dotenv import load_dotenv


load_dotenv()

API_TOKEN = os.getenv("API_KEY")
API_URL = f"https://api.telegram.org/bot{API_TOKEN}/sendMessage"

def send_message(chat_id: int, text: str):
    data = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(API_URL, params=data)
