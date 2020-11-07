import os

import telebot
from dotenv import load_dotenv

from bot_top_ranking.config_class import State

load_dotenv()
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))
state = State()
