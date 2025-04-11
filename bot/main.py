import os
import logging
import telebot
from dotenv import load_dotenv

from bot.notifier import notify_admin
from bot.responder import get_openai_client, generate_response

# Логирование
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/bot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# Переменные окружения
load_dotenv()
TOKEN_TG = os.getenv("TOKEN_TG")
OPENAI_KEY = os.getenv("OPENAI_KEY")

if not TOKEN_TG or not OPENAI_KEY:
    logging.error("❌ Переменные окружения не заданы")
    exit(1)

bot = telebot.TeleBot(TOKEN_TG)
client = get_openai_client(OPENAI_KEY)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Привет! Напиши любое имя — я попробую шуточно доказать, что оно скандинавское!"
    )

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text.strip()
    username = message.from_user.username or "без ника"
    prompt = f"Шуточно докажи, что имя {user_input} — скандинавское."
    logging.info(f"Запрос от @{username}: {user_input}")

    try:
        response = generate_response(client, prompt)
        bot.send_message(message.chat.id, response)
    except Exception as e:
        logging.exception("Ошибка при генерации ответа")
        bot.send_message(message.chat.id, "⚠️ Упс! Что-то пошло не так.")
        notify_admin(f"❌ Ошибка у @{username}:\n{e}")

if __name__ == "__main__":
    try:
        logging.info("🤖 Бот запущен")
        bot.polling(none_stop=True)
    except Exception as e:
        logging.critical("Бот упал критически", exc_info=e)
        notify_admin(f"🚨 Критическая ошибка бота:\n{e}")
