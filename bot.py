import os
import logging
import telebot
from dotenv import load_dotenv
import openai

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/bot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

load_dotenv()
TOKEN_TG = os.getenv("TOKEN_TG")
OPENAI_KEY = os.getenv("OPENAI_KEY")

if not TOKEN_TG or not OPENAI_KEY:
    logging.error("❌ Не найдены переменные окружения TOKEN_TG или OPENAI_KEY")
    exit(1)

client = openai.OpenAI(api_key=OPENAI_KEY)

bot = telebot.TeleBot(TOKEN_TG)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Привет! Я бот, который попробует шуточно доказать, что имя скандинавское.\nНапиши любое имя:"
    )

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text.strip()
    prompt = f"Шуточно докажи, что имя {user_input} — скандинавское."

    logging.info(f"Запрос от @{message.from_user.username or 'anon'}: {user_input}")

    try:
        response = generate_response(prompt)
        bot.send_message(message.chat.id, response)
    except Exception as e:
        logging.exception("Ошибка при генерации ответа")
        bot.send_message(message.chat.id, "⚠️ Упс! Что-то пошло не так. Попробуй снова позже.")

def generate_response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.9,
        max_tokens=500,
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    logging.info("🤖 Бот запущен и ждёт сообщений...")
    bot.polling(none_stop=True)
