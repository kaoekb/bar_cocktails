import os
import logging
import telebot
from dotenv import load_dotenv
import openai

# Загрузка переменных окружения из .env
load_dotenv()
TOKEN_TG = os.getenv("TOKEN_TG")
OPENAI_KEY = os.getenv("OPENAI_KEY")

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация OpenAI клиента
client = openai.OpenAI(api_key=OPENAI_KEY)

# Инициализация бота
bot = telebot.TeleBot(TOKEN_TG)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Привет! Я бот, который попробует шуточно доказать, что имя скандинавское. Введите имя:"
    )

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text.strip()
    prompt = f"Шуточно докажи, что имя {user_input} — скандинавское."

    try:
        response = generate_response(prompt)
        bot.send_message(message.chat.id, response)
    except Exception as e:
        logging.exception("Ошибка при генерации ответа")
        bot.send_message(message.chat.id, "Упс! Что-то пошло не так. Попробуй снова позже.")

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
    bot.polling(none_stop=True)
