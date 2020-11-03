# import os
import os

from bot_top_ranking.handlers import bot
import time
import pytest
# from dotenv import load_dotenv
from telebot import TeleBot, types


#
# load_dotenv()
#
# should_skip = 'BOT_TOKEN' not in os.environ
# COUNT_MUSIC = state.config["count_music"]
# if not should_skip:
#     TOKEN = os.environ['BOT_TOKEN']
#     CHAT_ID = os.environ['CHAT_ID']
#
from tests.bot.test_handlers import CHAT_ID


@pytest.fixture(autouse=True)
def set_mock_send_message(mocker, mock_message):
    def stub_send_message(chat_id, message, *args, **kwargs):
        print(message, end='')
        return mock_message
    mocker.patch.object(bot, 'send_message', new=stub_send_message)


@pytest.fixture(scope="session", name="mock_message")
def create_mock_message():
    params = {'text': 'Test message'}
    bot_id = bot.get_me()
    chat = types.Chat(CHAT_ID, 'supergroup')
    return types.Message(1, bot_id, None, chat, '', params, "")


@pytest.fixture(name="mock_call")
def create_mock_call(mock_message):
    bot_id = bot.get_me()
    chat = types.Chat(os.getenv("CHAT_ID"), 'supergroup')
    return types.CallbackQuery(1, bot_id, "help", chat, mock_message)