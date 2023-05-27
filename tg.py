import logging
import os
import traceback
import telebot

from time import time

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN') 

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def send_message_sync(chat_id, message):
    bot.send_message(chat_id, message)

def send_audio_sync(chat_id, path):
    audio = open( path, 'rb' )
    bot.send_audio(chat_id, audio)
    audio.close()
    os.system(f"rm '{path}'")

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.chat.id)

def start():
    while True:
        try:
            bot.infinity_polling()
        except Exception:
            send_message_sync(os.getenv('TG_ADMIN_ID'), f"telegram: \n{traceback.format_exc()}")