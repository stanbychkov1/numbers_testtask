import os

from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_API_KEY = os.environ.get('TELEGRAM_API_KEY')
CHAT_ID = os.environ.get('CHAT_ID')


def send_message(message):
    bot = Bot(token=TELEGRAM_API_KEY)
    chat_id = CHAT_ID
    text = f'{message} не отправлен!'
    bot.send_message(chat_id, text)
