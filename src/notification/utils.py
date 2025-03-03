import os
import requests
from dotenv import load_dotenv


load_dotenv()

API_TOKEN = os.getenv("API_KEY")
API_URL = f"https://api.telegram.org/bot{API_TOKEN}/"

def send_message(chat_id: int, text: str):
    data = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(API_URL + "sendMessage", params=data)


def get_bot_username() -> str:
    req = requests.get(API_URL + "getMe")
    return req.json()["result"]["username"]
