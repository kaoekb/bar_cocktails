import os
import requests
from dotenv import load_dotenv

load_dotenv()
ADMIN_ID = os.getenv("ADMIN_ID")
BOT_TOKEN = os.getenv("TOKEN_TG")

def notify_admin(text: str):
    if not ADMIN_ID or not BOT_TOKEN:
        return
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {"chat_id": ADMIN_ID, "text": text}
        requests.post(url, data=data, timeout=5)
    except Exception as e:
        print("Ошибка при отправке уведомления админу:", e)
