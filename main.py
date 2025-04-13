import os
import logging
import random
import telebot

from dotenv import load_dotenv
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from bot.cocktails import cocktails
from bot.notifier import notify_admin
from bot.responder import (
    get_openai_client,
    generate_response,
    generate_image_url,
    generate_image_sticker
)

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
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("🌍 Открыть меню миров"))

    bot.send_message(
        message.chat.id,
        "👋 Привет! Напиши любое имя — я попробую шуточно доказать, что именно этот коктейль или настойка подходит для тебя!\n\n"
        "🌟 Или выбери, куда хочешь отправиться:",
        reply_markup=markup
    )


@bot.message_handler(func=lambda message: message.text == "🌍 Открыть меню миров")
def menu_button_handler(message):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("🛡️ В Скандинавию", url="https://t.me/name_scandi_bot"),
        InlineKeyboardButton("🌾 В Славянщину", url="https://t.me/name_slavic_bot"),
        InlineKeyboardButton("🍀 В Кельтию", url="https://t.me/name_kelt_bot")
    )

    bot.send_message(
        message.chat.id,
        "⚔️ Три пути открыты перед тобой, путник:\n"
        "Выбери, в каком мире хочешь узнать тайны имён.",
        reply_markup=markup
    )


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "🌍 Открыть меню миров":
        return

    user_input = message.text.strip()
    username = message.from_user.username or "без ника"
    chosen = random.choice(cocktails)

    logging.info(f"Запрос от @{username}: {user_input}")

    try:
        # Текстовая часть
        prompt = (
            f"Имя пользователя: {user_input}.\n"
            f"Коктейль: {chosen}.\n"
            f"Придумай шуточное, но правдоподобное объяснение, почему именно этот коктейль или настойка подходит этому человеку. "
            f"Пиши от имени бармена, можешь использовать юмор, легкую иронию и вдохновляющий стиль."
        )
        response = generate_response(client, prompt)
        bot.send_message(message.chat.id, response)

        # Промпт для картинки
        image_prompt = (
            f"Ведьминский дарк-фэнтези арт, где имя «{user_input}» написано на книге, зелье или амулете. "
            f"Атмосфера магии, свечи, дым, луна, лес, таинственный свет. Высокая детализация, стиль dark fantasy."
        )
        # sticker_prompt = (
        #     f"Магический персонаж по имени «{user_input}». "
        #     f"Тёмный герой или ведьма, в стиле дарк-фэнтези. "
        #     f"Портрет по пояс, выразительное лицо, мистический взгляд, магический амулет, "
        #     f"атмосферный свет, фон затемнён. Стиль: концепт-арт."
        # )
        
        # sticker_prompt = (
        #     f"Магический персонаж по имени «{user_input}», вдохновлённый напитком «{chosen}». "
        #     f"Персонаж в стиле дарк-фэнтези, с чертами, отражающими суть напитка. "
        #     f"Художественный портрет по пояс: выразительные глаза, магический атрибут, костюм, "
        #     f"символика и цвета, передающие настроение напитка. Стиль — атмосферный концепт-арт, "
        #     f"приглушённый фон, мистический свет. Без фона. Идеально подходит для Telegram-стикера."
        # )
        
        sticker_prompt = (
            f"Стикер в стиле мультяшной ведьмы по имени «{user_input}», вдохновлённой напитком «{chosen}». "
            f"Герой улыбается, делает гримасу или подмигивает. Шапка ведьмы, зелье в руке, смешной магический эффект. "
            f"Весёлый стиль, крупные глаза, яркие цвета, простая форма. Без фона. Идеально подходит для Telegram-стикера."
        )

        # Сначала картинка
        image_url = generate_image_url(client, image_prompt)
        bot.send_photo(message.chat.id, image_url, caption="🧙 Вот твоё ведьминское видение...")

        # Затем стикер
        sticker = generate_image_sticker(client, sticker_prompt)
        bot.send_sticker(message.chat.id, sticker)
        
    except Exception as e:
        logging.exception("Ошибка при генерации ответа или изображения")
        bot.send_message(message.chat.id, "⚠️ Упс! Что-то пошло не так.")
        notify_admin(f"❌ Ошибка у @{username}:\n{e}")


if __name__ == "__main__":
    try:
        logging.info("🤖 Бот запущен")
        bot.polling(none_stop=True, skip_pending=True)
    except Exception as e:
        logging.critical("Бот упал критически", exc_info=e)
        notify_admin(f"🚨 Критическая ошибка бота:\n{e}")
