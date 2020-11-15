import unittest
import os
import time
import csv

import telebot

from bot_top_ranking import work_with_csv
from bot_top_ranking.handlers import state

from unittests.conf import call, message, chat, user
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
        os.remove(self.csv_filename)

    
    def test_get_music_csv(self):
        test_song = {
            'author' : 'Imagine Dragons',
            'title' : 'Demons',
            'link' : 'www.com'
        }

        expected_result = {
            'author' : 'Imagine Dragons',
            'title' : 'Demons',
            'link' : 'www.com',
            'mark' : 0,
            'pos' : 1,
            'voted_users' : []
        }

        with open(self.csv_filename, mode="w", encoding='utf-8') as w_file:
            names = ["title", "author", "link"]
            csv_writer = csv.DictWriter(w_file, delimiter=',', lineterminator='\r', fieldnames=names)
            csv_writer.writeheader()
            csv_writer.writerow(test_song)

        
        self.assertEqual(len(work_with_csv.get_music_csv(self.csv_filename)), 1)
        self.assertEqual(work_with_csv.get_music_csv(self.csv_filename)[0],expected_result)
        os.remove(self.csv_filename)