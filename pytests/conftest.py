import json
import os

import pytest
from dotenv import load_dotenv
from telebot import types

from bot_top_ranking.utils import bot, state

load_dotenv()

CHAT_ID = os.getenv("CHAT_ID")


@pytest.fixture(autouse=True)
def set_mock_send_message(mocker, mock_message):
    def stub_send_message(chat_id, message, *args, **kwargs):
        print(message, end='')
        return mock_message

    mocker.patch.object(bot, 'send_message', new=stub_send_message)


@pytest.fixture(scope="module", name="mock_message")
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


@pytest.fixture(scope="session", autouse=True)
def set_temp_folder(tmpdir_factory):
    temp_folder = tmpdir_factory.mktemp('temporary_config')
    configs_folder = temp_folder.mkdir("configs")
    json_config = configs_folder.join("default_config.json")
    json_config_to_save = configs_folder.join("saved_config.json")
    json_data = json.load(open(os.getenv("DEFAULT_JSON")))
    json_config.write(json.dumps(json_data, indent=4))
    state.__init__(path_to_save_config=json_config_to_save)
    state.save_config()
    yield json_config_to_save
    # shutil.rmtree(tmpdir_factory.getbasetemp())  # /tmp/pytest-of-kiryl/ base temp dir


@pytest.fixture(name="config", autouse=True)
def set_default_state(set_temp_folder):
    path_to_config = set_temp_folder
    state.__init__(path_to_config=path_to_config)
