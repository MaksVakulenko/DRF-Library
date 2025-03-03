import os
import requests
from celery import shared_task
from dotenv import load_dotenv


load_dotenv()

API_TOKEN = os.getenv("API_KEY")
API_URL = f"https://api.telegram.org/bot{API_TOKEN}/"

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_message(self, chat_id: int, text: str):
    data = {
        "chat_id": chat_id,
        "text": text
    }
    try:
        response = requests.post(API_URL + "sendMessage", params=data)

        if response.status_code != 200:
            raise self.retry(exc=f"Received status code {response.status_code} instead of 200.")

        return response.json()

    except Exception as exc:
        raise self.retry(exc=exc)


def get_bot_username() -> str:
    req = requests.get(API_URL + "getMe")
    return req.json()["result"]["username"]
