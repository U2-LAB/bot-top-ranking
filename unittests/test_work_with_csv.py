import unittest
import os
import time

import telebot

from bot_top_ranking import work_with_csv
from bot_top_ranking.handlers import state

from .conf import call, message, chat, user
from unittest import skip
from dotenv import load_dotenv

load_dotenv()

class TestWorkWithCsv(unittest.TestCase):
    def setUp(self):
        self.amount = 25
        self.csv_filename = "Test.csv"

    def test_create_csv(self):
        work_with_csv.create_csv(self.csv_filename, self.amount)
        
        self.assertTrue(os.path.exists(self.csv_filename))
    
    def test_get_music_csv(self):
        self.assertEqual(len(work_with_csv.get_music_csv(self.csv_filename)), self.amount)

    