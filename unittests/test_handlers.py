import unittest
import os
import time

import telebot

from bot_top_ranking import handlers
from bot_top_ranking.handlers import state

from bot_top_ranking.help_functions import create_top
from bot_top_ranking.work_with_csv import get_music_csv

from .conf import (
    call, 
    message, 
    chat, 
    mock_upload_song, 
    user, 
    mock_send_message, 
    mock_pin_chat_message, 
    get_capture, 
    mock_state_init,
    mock_unpin_chat_message,
    mock_promote_chat_member,
    mock_set_chat_administrator_custom_title,
    mock_send_audio, 
    mock_download_music_link,
    get_songs
)
from unittest import skip
from unittest.mock import patch
from dotenv import load_dotenv

load_dotenv()



class TestHandlers(unittest.TestCase):
    def setUp(self):
        self.bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))
        self.User = user()
        self.Chat = chat()
        self.Message = message(self.User,self.Chat)

    
    @patch('bot_top_ranking.handlers.bot.send_message', side_effect=mock_send_message)
    def test_get_help(self, mock_message):
        handlers.get_help(self.Message)
        capture = get_capture()
        expected_output = (
            "<b>Admin commands</b>\n"
            "/disco to start poll\n"
            "/poptop [num] output referenced song (e.g. /poptop or /poptop 5)\n"
            "/finish to end poll\n"
            "/setDJ [mentioned user] set mentioned people a DJ (e.g. /setDJ @Admin)\n"
            "/settings_mp3 on|off (e.g. /settings_mp3 or /settings_mp3 on)\n"
            "/poll_status to print status of poll in this chat\n"
            "<b>User commands</b>\n"
            "/top [num] output top songs(e.g. /top 5)\n"
            "/vote [num] vote for song from poll (e.g. /vote 5)\n"
        )
        self.assertEqual(capture,expected_output)
    
    @patch('bot_top_ranking.handlers.bot.send_message', side_effect=mock_send_message)
    def test_callback_query(self, mock_message):
        Call = call(self.User,"help",self.Chat,self.Message)
        self.assertIsNone(handlers.callback_query(Call))
        capture = get_capture()
        expected_output = (
            "<b>Admin commands</b>\n"
            "/disco to start poll\n"
            "/poptop [num] output referenced song (e.g. /poptop or /poptop 5)\n"
            "/finish to end poll\n"
            "/setDJ [mentioned user] set mentioned people a DJ (e.g. /setDJ @Admin)\n"
            "/settings_mp3 on|off (e.g. /settings_mp3 or /settings_mp3 on)\n"
            "/poll_status to print status of poll in this chat\n"
            "<b>User commands</b>\n"
            "/top [num] output top songs(e.g. /top 5)\n"
            "/vote [num] vote for song from poll (e.g. /vote 5)\n"
        )
        self.assertEqual(capture,expected_output)
    
    @patch('bot_top_ranking.handlers.bot.pin_chat_message', sedi_effect=mock_pin_chat_message)
    @patch('bot_top_ranking.handlers.bot.send_message', side_effect=mock_send_message)
    def test_create_poll(self, mock_message, smth):
        state.config['poll_started'] = False
        self.assertIsNone(handlers.create_poll(self.Message))
        
        capture = get_capture()

        music_poll = ''
        for idx, song in enumerate(state.config["songs"]):
            music_poll += f'{idx + 1}. {song["author"]} | {song["title"]}\n'
        self.assertEqual(capture,music_poll)

    @patch('bot_top_ranking.handlers.bot.pin_chat_message', sedi_effect=mock_pin_chat_message)
    @patch('bot_top_ranking.handlers.bot.send_message', side_effect=mock_send_message)
    def test_create_poll_raise(self,mock_message, smth):
        state.config['poll_started'] = True
        self.assertIsNone(handlers.create_poll(self.Message))

        capture = get_capture()
        expected_capture = "Previous poll hasn't finished yet. Type /finish or use pined Message"
        self.assertEqual(capture, expected_capture)



    @patch('bot_top_ranking.handlers.bot.pin_chat_message', sedi_effect=mock_pin_chat_message)
    @patch('bot_top_ranking.handlers.bot.send_message', side_effect=mock_send_message)
    def test_get_songs_top_list(self,mock_message, smth):
        params = [1, 12, 23, 567]
        
        state.config["songs"] = get_songs()
        state.config['poll_started'] = True
        
        for param in params:
            with self.subTest():
                _message = message(self.User,self.Chat,f'/top {param}'.strip())
                self.assertIsNone(handlers.get_songs_top_list(_message))
                
                capture = get_capture()
                
                music_poll = ''
                top_list = create_top(state.config["songs"])
                for idx, song in enumerate(top_list[:param]):
                    music_poll += f'{idx + 1}. {song["author"]} | {song["title"]} | {song["mark"]} Votes\n'
                self.assertEqual(capture,music_poll)

    @patch('bot_top_ranking.handlers.bot.pin_chat_message', sedi_effect=mock_pin_chat_message)
    @patch('bot_top_ranking.handlers.bot.send_message', side_effect=mock_send_message)
    def test_get_songs_top_list_wrong(self,mock_message,mockk_pin):
        params = [0,'qwerty','']
        state.config['poll_started'] = False
        
        self.assertIsNone(handlers.create_poll(self.Message))
        self.assertTrue(state.config["poll_started"])

        for param in params:
            with self.subTest():
                _message = message(self.User,self.Chat,f'/top {param}'.strip())
                self.assertIsNone(handlers.get_songs_top_list(_message))

                capture = get_capture()

                self.assertEqual(capture,'Incorrect input. Type /help to get information about commands')

    def test_vote_for_song(self):
        state.config["songs"] = get_songs()
        state.config['poll_started'] = True
        
        song_id = 1 # song #2 because array start from 0
        begin_mark = state.config["songs"][song_id]["mark"]
        
        vote_message = message(self.User,self.Chat,'/vote 2')

        self.assertIsNone(handlers.vote_for_song(vote_message))
        self.assertEqual(begin_mark+1, state.config["songs"][song_id]["mark"])

    def test_unvote_song(self):
        state.config["songs"] = get_songs()
        state.config['poll_started'] = True

        song_id = 2
        begin_mark = state.config["songs"][song_id]["mark"]
        vote_message = message(self.User,self.Chat,'/vote 3')

        self.assertIsNone(handlers.vote_for_song(vote_message))
        self.assertEqual(begin_mark+1, state.config["songs"][song_id]["mark"])

        self.assertIsNone(handlers.vote_for_song(vote_message))
        self.assertEqual(begin_mark, state.config["songs"][song_id]["mark"])

    @patch('bot_top_ranking.handlers.bot.send_message', side_effect=mock_send_message)
    def test_pervote_song(self,mock_message):
        state.config['songs'] = get_songs()
        state.config['poll_started'] = True

        vote_message = message(self.User,self.Chat,'/vote 88889')

        self.assertIsNone(handlers.vote_for_song(vote_message))
        self.assertFalse(any([song['mark'] for song in state.config['songs']]))
        capture = get_capture()
        expected_output = f'Number should be less than {state.config["count_music"]} and greater than 0'
        self.assertEqual(capture, expected_output)

    @patch('bot_top_ranking.handlers.bot.pin_chat_message', side_effect=mock_pin_chat_message)
    @patch('bot_top_ranking.help_functions._download_music_link',side_effect=mock_download_music_link)
    @patch('bot_top_ranking.handlers.bot.send_audio', side_effect=mock_send_audio)
    @patch('bot_top_ranking.handlers.bot.send_message', side_effect=mock_send_message)
    def test_pop_element_from_top_notupload(self,mock_message, mock_audio, down_link, pin):
        

        state.config["songs"] = get_songs()
        params = [1, 5, 12]
        for param in params:
            with self.subTest():
                # print(state.config["songs"])
                state.config['poll_started'] = True

                poptop_message = message(self.User, self.Chat, f'/poptop {param}'.strip())
                self.assertIsNone(handlers.pop_element_from_top(poptop_message))
                capture = get_capture()
                top_list = create_top(state.config["songs"])
                
                expected_output = top_list[param-1]['author'] + ' | ' + top_list[param-1]['title']
                self.assertEqual(capture,expected_output)

    @patch('bot_top_ranking.help_functions.upload_song', side_effect=mock_upload_song)
    @patch('bot_top_ranking.handlers.bot.send_message', side_effect=mock_send_message)
    def test_pop_element_from_top_upload(self,mock_message, mock_upload):
        state.config["songs"] = get_songs()
        state.config['upload_flag'] = True
        
        params = [1, 5, 12]
        for param in params:
            with self.subTest():
                # print(state.config["songs"])
                state.config['poll_started'] = True

                poptop_message = message(self.User, self.Chat, f'/poptop {param}'.strip())
                self.assertIsNone(handlers.pop_element_from_top(poptop_message))
                capture = get_capture('upload_song.txt')
                top_list = create_top(state.config["songs"])
                
                expected_output = top_list[param-1]['author'] + ' | ' + top_list[param-1]['title']
                self.assertEqual(capture,expected_output)

    @patch('bot_top_ranking.handlers.bot.pin_chat_message', sedi_effect=mock_pin_chat_message)
    @patch('bot_top_ranking.help_functions._download_music_link',side_effect=mock_download_music_link)
    @patch('bot_top_ranking.handlers.bot.send_audio', side_effect=mock_send_audio)
    @patch('bot_top_ranking.handlers.bot.send_message', side_effect=mock_send_message)
    def test_pop_element_from_top_empty(self,mock_message, mock_audio, down_link, pin):
        
        state.config["songs"] = get_songs()
        state.config['poll_started'] = True

        poptop_message = message(self.User, self.Chat, '/poptop')
        self.assertIsNone(handlers.pop_element_from_top(poptop_message))

        capture = get_capture()
        top_list = create_top(state.config["songs"])
        
        expected_output = top_list[0]['author'] + ' | ' + top_list[0]['title']
        self.assertEqual(capture,expected_output)

    @patch('bot_top_ranking.handlers.bot.pin_chat_message', sedi_effect=mock_pin_chat_message)
    @patch('bot_top_ranking.help_functions._download_music_link',side_effect=mock_download_music_link)
    @patch('bot_top_ranking.handlers.bot.send_audio', side_effect=mock_send_audio)
    @patch('bot_top_ranking.handlers.bot.send_message', side_effect=mock_send_message)
    def test_pop_element_from_top_unnumber(self,mock_message, mock_audio, down_link, pin):
        
        state.config["songs"] = get_songs()
        state.config['poll_started'] = True

        poptop_message = message(self.User, self.Chat, '/poptop 22222')
        self.assertIsNone(handlers.pop_element_from_top(poptop_message))

        capture = get_capture()
        top_list = create_top(state.config["songs"])
        
        expected_output = f'Number should be less than {state.config["count_music"]} and greater than 0'
        self.assertEqual(capture,expected_output)




    @patch('bot_top_ranking.handlers.bot.unpin_chat_message',side_effect=mock_unpin_chat_message)
    @patch('bot_top_ranking.handlers.bot.send_message', side_effect=mock_send_message)
    @patch('bot_top_ranking.handlers.state.__init__',side_effect=mock_state_init)
    def test_finish_poll(self,mock_message, mock_state, mock_unpin):
        
        state.config["poll_started"] = True

        self.assertIsNone(handlers.finish_poll(self.Message))
        self.assertFalse(state.config['poll_started'])
        self.assertFalse(any([song['mark'] for song in state.config['songs']]))
        capture = get_capture()
        expected_output = 'Poll was finished'
        self.assertEqual(capture,expected_output)

    @patch('bot_top_ranking.handlers.bot.send_message', side_effect=mock_send_message)
    def test_change_upload_flag(self, mock_message):
        state.config["songs"] = get_songs()
        state.config['poll_started'] = True

        params = ['off', 'on', '', 123]
        for param in params:
            with self.subTest():
                change_message = message(self.User,self.Chat,text=f'/settings_mp3 {param}'.strip())
                started_upload_flag = state.config['upload_flag']
                self.assertIsNone(handlers.change_upload_flag(change_message))
                capture = get_capture()
                expected_output = f'uploading songs is <b>{"Enabled" if state.config["upload_flag"] else "Disabled"}</b>'
                if param == 'off':
                    self.assertFalse(state.config['upload_flag'])
                    self.assertEqual(capture,expected_output)
                elif param == 'on':
                    self.assertTrue(state.config['upload_flag'])
                    self.assertEqual(capture,expected_output)
                elif param == '':
                    self.assertTrue(not started_upload_flag == state.config['upload_flag'])
                    self.assertEqual(capture,expected_output)
                else:
                    self.assertTrue(started_upload_flag == state.config['upload_flag'])
                    self.assertEqual(capture,expected_output)
    
    @patch('bot_top_ranking.handlers.bot.send_message', side_effect=mock_send_message)
    def test_get_poll_status(self, mock_message):
        self.assertIsNone(handlers.get_poll_status(self.Message))
        capture = get_capture()

        expected_output = (
            'Poll status\n'
            '———————————\n'
            f'Poll started: {state.config["poll_started"]}\n'
            f'Upload mp3: {"on" if state.config["upload_flag"] else "off"}'
        )
        self.assertEqual(capture,expected_output)


    @patch('bot_top_ranking.handlers.bot.send_message', side_effect=mock_send_message)
    def test_set_dj_by_user_id(self,mock_message):
        user_tag = 'admin'
        mentioned_message = message(user(username='admin'),self.Chat,f'/setDJ @{user_tag}')
        self.assertIsNone(handlers.set_dj_by_user_id(mentioned_message))        
        self.assertEqual(state.config["users_for_promoting"][-1],user_tag)
        capture = get_capture()
        expected_output = f'@{user_tag} type /becomeDJ. It\'s privileges only for you ^_^'
        self.assertEqual(capture,expected_output)

    @patch('bot_top_ranking.handlers.bot.send_message', side_effect=mock_send_message)
    def test_set_dj_by_user_id_incorrect(self, mock_message):
        params = ['']
        for param in params:
            with self.subTest():
                mentioned_message = message(self.User,self.Chat,f'/setDJ @{param}')
                self.assertIsNone(handlers.set_dj_by_user_id(mentioned_message))
                capture = get_capture()
                expected_output = 'Incorrect input. Type /help to get information about commands'
                self.assertEqual(capture,expected_output)


    @patch('bot_top_ranking.handlers.bot.set_chat_administrator_custom_title', side_effect=mock_set_chat_administrator_custom_title)
    @patch('bot_top_ranking.handlers.bot.promote_chat_member', side_effect=mock_promote_chat_member)
    @patch('bot_top_ranking.handlers.bot.send_message', side_effect=mock_send_message)
    def test_become_dj(self, mock_message,mock_promote,mock_title):
        
        user_tag = 'nikefr7'
        state.config['users_for_promoting']=[user_tag]

        
        self.assertIsNone(handlers.become_dj(self.Message))
        self.assertFalse(state.config['users_for_promoting'])
        capture = get_capture()
        expected_output = f'@{user_tag} You have been promoted to DJ. Congratulate 🏆🏆🏆'
        self.assertEqual(capture,expected_output)

    @patch('bot_top_ranking.handlers.bot.set_chat_administrator_custom_title', side_effect=mock_set_chat_administrator_custom_title)
    @patch('bot_top_ranking.handlers.bot.promote_chat_member', side_effect=mock_promote_chat_member)
    @patch('bot_top_ranking.handlers.bot.send_message', side_effect=mock_send_message)
    def test_become_dj_cannot(self, mock_message,mock_promote,mock_title):
        state.config['users_for_promoting']=['nikefr7']

        self.assertIsNone(handlers.become_dj(message(user(username='qwerty'),self.Chat)))
        capture = get_capture()
        expected_output = "You cannot use this command"
        self.assertEqual(capture,expected_output)

    @patch('bot_top_ranking.handlers.bot.set_chat_administrator_custom_title', side_effect=mock_set_chat_administrator_custom_title)
    @patch('bot_top_ranking.handlers.bot.promote_chat_member', side_effect=mock_promote_chat_member)
    @patch('bot_top_ranking.handlers.bot.send_message', side_effect=mock_send_message)
    def test_become_dj_raise(self, mock_message,mock_promote,mock_title):
        state.config['users_for_promoting']=['nikefr7']

        self.assertIsNone(handlers.become_dj(message(user(username='nikefr7',id=666),self.Chat)))
        capture = get_capture()
        expected_output = 'You are admin. Why do you try to do it??? (╮°-°)╮┳━━┳ ( ╯°□°)╯ ┻━━┻'
        self.assertEqual(capture,expected_output)

    