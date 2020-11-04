import unittest
import os
import time

import telebot
from telebot import types

from bot_top_ranking import help_functions
from bot_top_ranking.handlers import state

from .conf import (
    message,
    chat,
    user,
    mock_download_music_link,
    mock_send_audio,
    get_capture,
)
from unittest import skip
from unittest.mock import patch, Mock
from dotenv import load_dotenv

load_dotenv()

class TestHelpFunctions(unittest.TestCase):
    def setUp(self):
        self.bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))
        self.User = user()
        self.Chat = chat()
        self.Message = message(self.User,self.Chat)
    
    def test_gen_markup(self):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row_width = 1
        keyboard.add(types.InlineKeyboardButton("Help", callback_data="help"),)
        self.assertEqual(help_functions.gen_markup().__dict__, keyboard.__dict__)

    def test_download_music_link(self):
        link = 'https://zaycev.net/musicset/dl/65f2858273af4c1747dcf013b4402a88/21847355.json'
        file_name = 'author - title.mp3'
        self.assertIsNone(help_functions._download_music_link(link,file_name))
        self.assertTrue(os.path.exists(file_name))


    @patch('bot_top_ranking.help_functions._download_music_link',side_effect=mock_download_music_link)
    def test_upload_song(self, mock_dwnld):
        song = {
            "title" : "title",
            "author" : "author",
            "link" : 'https://zaycev.net/musicset/dl/65f2858273af4c1747dcf013b4402a88/21847355.json',
            "mark" : 5,
            "pos" : 1
        }        
        mock_bot = Mock()
        mock_bot.send_audio = mock_send_audio
        self.assertIsNone(help_functions.upload_song(song,mock_bot,state))
        capture_upload = get_capture('song.txt')
        self.assertEqual(capture_upload,'Audio')

    def test_create_top(self):
        songs = [
            {
                "title" : "title",
                "author" : "author",
                "link" : 'https://zaycev.net/musicset/dl/65f2858273af4c1747dcf013b4402a88/21847355.json',
                "mark" : 1,
                "pos" : 1
            },
            {
                "title" : "title",
                "author" : "author",
                "link" : 'https://zaycev.net/musicset/dl/65f2858273af4c1747dcf013b4402a88/21847355.json',
                "mark" : 2,
                "pos" : 1
            }   ,
            {
                "title" : "title",
                "author" : "author",
                "link" : 'https://zaycev.net/musicset/dl/65f2858273af4c1747dcf013b4402a88/21847355.json',
                "mark" : 3,
                "pos" : 1
            }
        ]
        self.assertEqual(help_functions.create_top(songs),songs[::-1])

    def test_create_empty_top(self):
        songs = []
        self.assertEqual(help_functions.create_top(songs),songs[::-1])
