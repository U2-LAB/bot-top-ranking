import unittest
import os

import telebot

from bot_top_ranking import decorators
from bot_top_ranking.handlers import state
from telebot import types

from collections import namedtuple


from .conf import (
    message, 
    chat, 
    user, 
    mock_send_message, 
    get_capture, 

)
from unittest import skip
from unittest.mock import patch, Mock
from dotenv import load_dotenv

load_dotenv()
User = namedtuple('User', ['user'])

class TestDecorators(unittest.TestCase):
    def setUp(self):
        self.bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))
        self.User = user()
        self.Chat = chat()
        self.Message = message(self.User,self.Chat)

    
    def test_get_state(self):
        bot = Mock()
        bot.get_chat_administrators.return_value = []

        expected_result = ('state', 'bot')
        @decorators.get_state(*expected_result)
        def check_params():
            return decorators.get_state.state, decorators.get_state.bot
        
        self.assertEqual(check_params(),expected_result)

    def test_only_admin_decorator(self):
        bot = Mock()
        bot.get_chat_administrators.return_value = [User(types.User(bot.get_me().id, None, 'Tester'))]
        expected_output = "only_admin_achieved"
        bot.send_message = mock_send_message
        @decorators.only_admins
        @decorators.get_state(state, self.bot)
        def check_is_admin(message):
            bot.send_message(0, expected_output)

        check_is_admin(self.Message)
        capture = get_capture()
        self.assertEqual(capture,expected_output)

    def test_only_admin_decorator_raises(self):
        bot = Mock()
        bot.get_chat_administrators.return_value = []
        bot.send_message = mock_send_message
        
        expected_output = "You don't have permission"

        @decorators.only_admins
        @decorators.get_state(state,bot)
        def stub(message):
            print()

        stub(message(user(id=0),self.Chat))
        capture = get_capture()
        self.assertEqual(capture,expected_output)

    def test_started_poll_decorator(self):
        bot = Mock()
        bot.get_chat_administrators.return_value = []
        bot.send_message = mock_send_message

        expected_output = "started_pool_achieved"
        state.config["poll_started"] = True

        @decorators.started_pool
        @decorators.get_state(state, bot)
        def check_is_started(message):
            bot.send_message(0, expected_output)

        check_is_started(self.Message)
        capture = get_capture()
        self.assertEqual(capture, expected_output)

    def test_started_poll_decorator_raises(self):
        bot = Mock()
        bot.get_chat_administrators.return_value = []
        bot.send_message = mock_send_message

        expected_output = "Poll hasn't started yet. Type /disco to start"
        state.config["poll_started"] = False

        @decorators.started_pool
        @decorators.get_state(state, bot)
        def stub(message):
            print('smth')

        stub(self.Message)
        capture = get_capture()
        self.assertEqual(capture, expected_output)