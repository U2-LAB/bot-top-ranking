import unittest

from bot_top_ranking import decorators
from bot_top_ranking.handlers import state

from collections import namedtuple


from unittests.conf import (
    message, 
    chat, 
    user, 
    mock_send_message, 
    get_capture, 
    mocK_get_chat_administrators,
    mock_get_chat_administrators_empty
)
from unittest import skip
from unittest.mock import patch
from dotenv import load_dotenv
from bot_top_ranking.utils import bot

load_dotenv()
User = namedtuple('User', ['user'])

class TestDecorators(unittest.TestCase):
    def setUp(self):
        self.User = user()
        self.Chat = chat()
        self.Message = message(self.User,self.Chat)
    
    @patch('bot_top_ranking.utils.bot.send_message',side_effect=mock_send_message)
    @patch('bot_top_ranking.utils.bot.get_chat_administrators',side_effect=mocK_get_chat_administrators)
    def test_only_admin_decorator(self, mock_admin,mock_msg):
        expected_output = "only_admin_achieved"
        bot.send_message = mock_send_message
        @decorators.only_admins
        def check_is_admin(message):
            bot.send_message(0, expected_output)

        check_is_admin(self.Message)
        capture = get_capture()
        self.assertEqual(capture,expected_output)

    @patch('bot_top_ranking.utils.bot.send_message',side_effect=mock_send_message)
    @patch('bot_top_ranking.utils.bot.get_chat_administrators',side_effect=mock_get_chat_administrators_empty)
    def test_only_admin_decorator_raises(self, mock_admin, mock_msg):
        bot.send_message = mock_send_message
        
        expected_output = "You don't have permission"

        @decorators.only_admins
        def stub(message):
            print()

        stub(self.Message)
        capture = get_capture()
        self.assertEqual(capture,expected_output)

    @patch('bot_top_ranking.utils.bot.send_message',side_effect=mock_send_message)
    def test_started_poll_decorator(self, mock_msg):

        expected_output = "started_pool_achieved"
        state.config["poll_started"] = True

        @decorators.started_pool
        def check_is_started(message):
            bot.send_message(0, expected_output)

        check_is_started(self.Message)
        capture = get_capture()
        self.assertEqual(capture, expected_output)

    @patch('bot_top_ranking.utils.bot.send_message',side_effect=mock_send_message)
    def test_started_poll_decorator_raises(self, mock_msg):

        expected_output = "Poll hasn't started yet. Type /disco to start"
        state.config["poll_started"] = False

        @decorators.started_pool
        def stub(message):
            print('smth')

        stub(self.Message)
        capture = get_capture()
        self.assertEqual(capture, expected_output)