import collections
import json
import os
import telebot
import re
import math

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, MessageEntity
from work_music import get_links, download_music_link, get_music_csv

bot = telebot.TeleBot("1389559561:AAGbQ0mIBnptbQ4-XCvqKLlNMN-szSIhyxI")
ZERO = '\U00000030\U000020E3'
ONE = '\U00000031\U000020E3'
TWO = '\U00000032\U000020E3'
THREE = '\U00000033\U000020E3'
FOUR = '\U00000034\U000020E3'
FIVE = '\U00000035\U000020E3'
SIX = '\U00000036\U000020E3'
SEVEN = '\U00000037\U000020E3'
EIGHT = '\U00000038\U000020E3'
NINE = '\U00000039\U000020E3'

NUMBERS = [ZERO, ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE]

Song = collections.namedtuple('Song', ['link', 'title', 'mark', 'pos'])


class Setup:
    def __init__(self):
        self.config = {}
        self.loads_config()
        self.get_songs()

    def loads_config(self):
        with open("config.json") as r_file:
            self.config = json.load(r_file)
        self.users_for_promoting = self.config['usersForPromoting']
        self.count_music = self.config['countMusic']
        self.count_rows = self.config['countRows']
        self.current_page = self.config['currentPage']
        self.songs = self.config['songs']
        self.voted_users = self.config['votedUsers']
        self.current_idx = self.config['currentIdx']
        self.max_page = math.ceil(self.count_music / self.count_rows)
        self.poll_started = self.config['pollStarted']
        self.message_id = self.config['messageId']
        self.poll_id = self.config['pollId']
        self.chat_id = self.config['chatId']

    def get_songs(self):
        self.songs = get_music_csv("nikita.csv")


    


setup = Setup()


def get_emoji_number(number):
    return ''.join((list(map(lambda digit: NUMBERS[int(digit)], str(number)))))


def gen_markup():
    markup = InlineKeyboardMarkup(row_width=setup.count_rows)
    temp = setup.count_rows
    if setup.current_idx + setup.count_rows > setup.count_music:
        temp = setup.count_music - setup.current_idx + 1
    button_list = [
        InlineKeyboardButton(
            f'{get_emoji_number(setup.current_idx + idx)} - {setup.songs[setup.current_idx + idx - 1]["mark"]}',
            callback_data=setup.songs[setup.current_idx + idx - 1]["pos"]) for
        idx in range(temp)]
    markup.add(*button_list)
    if setup.current_page > 1 and setup.current_page < setup.max_page:
        markup.add(
            InlineKeyboardButton(f'prev page', callback_data='Prev page'),
            InlineKeyboardButton(f'next page', callback_data='Next page')
        )
    elif setup.current_page < setup.max_page:
        markup.add(InlineKeyboardButton(f'next page', callback_data='Next page'))
    else:
        markup.add(InlineKeyboardButton(f'prev page', callback_data='Prev page'))
    return markup


def check_admin_permissions(message):
    admins_id = [admin.user.id for admin in bot.get_chat_administrators(message.chat.id)]
    return message.from_user.id in admins_id


def update_pool_message(operation=None):
    music_pool = ''
    if operation == 'sub':
        setup.current_idx -= setup.count_rows
    elif operation == 'add':
        setup.current_idx += setup.count_rows
    for idx, song in enumerate(
            setup.songs[(setup.current_page - 1) * setup.count_rows: setup.current_page * setup.count_rows]):
        music_pool += f'{setup.current_idx + idx}. {song["title"]}\n'
    bot.edit_message_text(music_pool, setup.chat_id, setup.poll_id, reply_markup=gen_markup())


@bot.callback_query_handler(func=lambda call: True)
def get_callback_query(call):
    if not setup.poll_id:
        setup.poll_id = call.message.message_id
    if call.data == 'Next page':
        setup.current_page += 1
        update_pool_message(operation='add')
    elif call.data == 'Prev page':
        setup.current_page -= 1
        update_pool_message(operation='sub')
    elif (call.from_user.id, call.data) not in setup.voted_users:
        pos = int(call.data)
        song_item = setup.songs[pos]
        setup.songs[pos] = song_item._replace(mark=song_item.mark + 1)
        setup.voted_users.append((call.from_user.id, call.data))
    else:
        pos = int(call.data)
        song_item = setup.songs[pos]
        setup.songs[pos] = song_item._replace(mark=song_item.mark - 1)
        setup.voted_users.pop(setup.voted_users.index((call.from_user.id, call.data)))
    bot.answer_callback_query(call.id, f"Answer is {call.data}")
    if not call.data.endswith('page'):
        bot.edit_message_reply_markup(setup.chat_id, call.message.message_id, reply_markup=gen_markup())


@bot.message_handler(commands=['start'])
def get_start(message):
    bot.send_message(message.chat.id, r"Use /poll for starting poll of music")


@bot.message_handler(commands=['help'])
def get_help(message):
    bot.send_message(message.chat.id, r"Use /poll for starting poll of music")


@bot.message_handler(commands=['poll'])
def create_pool(message):
    if check_admin_permissions(message):
        if setup.poll_started:
            bot.send_message(message.chat.id, "Previous poll hasn't finished yet. Type /finish or use pinedMessage")
            return None
        setup.poll_started = True
        music_pool = ''
        for idx, song in enumerate(setup.songs[:setup.count_music]):
            music_pool += f'{idx}. {song["title"]} - {song["author"]}\n'
        poll = bot.send_message(message.chat.id, music_pool)
        setup.message_id = poll.message_id
        setup.chat_id = poll.chat.id
        bot.pin_chat_message(setup.chat_id, setup.message_id, disable_notification=True)
    else:
        bot.send_message(message.chat.id, r"You don't have permission")


@bot.message_handler(commands=['finish'])  # Unnecessary command
def finish_poll(message):
    if setup.poll_started:
        bot.unpin_chat_message(setup.chat_id)
        setup.make_default_setup()
    else:
        bot.send_message(setup.chat_id, "Pool hasn't started yet. Type /poll to start")


@bot.message_handler(commands=['top'])
def get_songs_top_list(message):
    top_list = setup.songs.copy()
    top_list.sort(key=lambda song: song["mark"], reverse=True)
    music_pool = ''
    try:
        top_number = int(re.search(r'^/top ([\d]*)$', message.text).group(1))
    except AttributeError:
        bot.send_message(message.chat.id, 'Incorrect input')
    else:
        if top_number > 10 or not top_number:
            bot.send_message(message.chat.id, 'Number should be greater than 0 and less or equal to 10')
        else:
            for idx, song in enumerate(top_list[:top_number]):  # 5 - regexp
                music_pool += f'{idx + 1}. {song["title"]} Votes - {song["mark"]}\n'
            bot.send_message(message.chat.id, music_pool)


@bot.message_handler(commands=['poptop'])
def pop_element_from_top(message):
    if check_admin_permissions(message):
        if setup.poll_started:
            try:
                if message.text == 'poptop':
                    idx = 0
                else:
                    idx = int(re.search(r'^/poptop ([\d]*)$', message.text).group(1)) - 1
            except AttributeError:
                bot.send_message(setup.chat_id, 'Incorrect input')
                return None
            else:
                if not idx or idx > setup.count_music:
                    bot.send_message(setup.chat_id, f'Type {setup.count_music} > number > 0')
                    return None
            is_changed = False
            top_list = setup.songs.copy()
            top_list.sort(key=lambda song: song["mark"], reverse=True)
            download_music_link(top_list[idx].link)
            audio = open('song.mp3', 'rb')
            bot.send_audio(message.chat.id, audio)
            os.remove('song.mp3')
            vote_remove_index_list = []
            for index, vote in enumerate(setup.voted_users):
                if vote[1] == top_list[idx].pos:  # vote[1] = song position
                    vote_remove_index_list.append(index)
                    song_item = setup.songs[int(vote[1])]
                    setup.songs[int(vote[1])] = song_item._replace(mark=0)
                    is_changed = True
            if is_changed:
                for index in vote_remove_index_list:
                    setup.voted_users.pop(index)
                bot.edit_message_reply_markup(setup.chat_id, setup.poll_id, reply_markup=gen_markup())
        else:
            bot.send_message(message.chat.id, "Pool hasn't started yet. Type /poll to start")
    else:
        bot.send_message(message.chat.id, r"You don't have permission")


@bot.message_handler(commands=['setDJ'])
def set_dj_by_user_id(message):
    if check_admin_permissions(message):
        mentioned_user = re.search(r'^/setDJ @([\w]*)', message.text).group(1)
        setup.users_for_promoting.append(mentioned_user)
        bot.send_message(message.chat.id, f'@{mentioned_user} type /becomeDJ. It\'s privileges only for you ^_^')


@bot.message_handler(commands=['becomeDJ'])
def become_dj(message):
    if message.from_user.username in setup.users_for_promoting:
        bot.promote_chat_member(message.chat.id, message.from_user.id, can_delete_messages=True)
        bot.set_chat_administrator_custom_title(message.chat.id, message.from_user.id, 'DJ')
        bot.send_message(
            message.chat.id,
            f'@{message.from_user.username} You have been promoted to DJ. Congratulate 🏆🏆🏆'
        )
    elif check_admin_permissions(message):
        bot.send_message(message.chat.id, 'You are admin. Why do you try to do it??? (╮°-°)╮┳━━┳ ( ╯°□°)╯ ┻━━┻')

def music_from_csv(path_csv : str) -> dict:
    pass

