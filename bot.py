import telebot
import os
import time

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from work_music import get_links, download_music_link

bot = telebot.TeleBot("1389559561:AAGbQ0mIBnptbQ4-XCvqKLlNMN-szSIhyxI", parse_mode=None)
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


class Setup:
    def __init__(self):
        self.count_music = 10
        self.count_rows = 3
        self.current_page = 1
        self.music_pos = [str(pos) for pos in range(self.count_music)]
        self.marks = [0 for _ in range(self.count_music)]
        self.voted_users = []
        self.start_idx = 1
        self.links = None
        self.titles = None
        self.max_page = self.count_music / self.count_rows

    def make_default_setup(self):
        self.count_music = 10
        self.count_rows = 3
        self.current_page = 1
        self.music_pos = [str(pos) for pos in range(self.count_music)]
        self.marks = [0 for _ in range(self.count_music)]
        self.voted_users = []
        self.start_idx = 1
        self.links = None
        self.titles = None
        self.max_page = self.count_music / self.count_rows


setup = Setup()


def get_emoji_number(number):
    return ''.join((list(map(lambda digit: NUMBERS[int(digit)], str(number)))))


def gen_markup():
    markup = InlineKeyboardMarkup(row_width=setup.count_rows)
    temp = setup.count_rows
    if setup.start_idx + setup.count_rows > setup.count_music:
        temp = setup.count_music - setup.start_idx + 1
    button_list = [
        InlineKeyboardButton(f'{get_emoji_number(setup.start_idx + idx)} - {setup.marks[setup.start_idx + idx - 1]}',
                             callback_data=setup.music_pos[setup.start_idx + idx - 1]) for
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


@bot.callback_query_handler(func=lambda call: True)
def get_callback_query(call):
    if call.data == 'Next page':
        setup.current_page += 1
        update_pool_message(call)
    elif call.data == 'Prev page':
        setup.current_page -= 1
        update_pool_message(call, oper='sub')
    elif (call.from_user.id, call.data) not in setup.voted_users:
        setup.marks[int(call.data)] += 1
        setup.voted_users.append((call.from_user.id, call.data))
    else:
        setup.marks[int(call.data)] -= 1
        setup.voted_users.pop(setup.voted_users.index((call.from_user.id, call.data)))
    bot.answer_callback_query(call.id, f"Answer is {call.data}")
    if not call.data.endswith('page'):
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=gen_markup())


@bot.message_handler(commands=['start'])
def get_start(message):
    bot.send_message(message.chat.id, r"Use /pool for starting pool of music")


@bot.message_handler(commands=['help'])
def get_help(message):
    bot.send_message(message.chat.id, r"Use /pool for starting pool of music")


def receive_top_music(chat_id):
    index_max = 0
    if not setup.voted_users:
        bot.send_message(chat_id, "No one voted\nLoading the first song")
    else:
        max_elem = max(setup.marks)
        index_max = setup.marks.index(max_elem)
        bot.send_message(chat_id,
                         f"The winning composition is ... 🥁'Bam'🥁'Bam'🥁'Bam'🥁'Bam'")

    download_music_link(setup.links[index_max], index_max)
    audio = open(f'{index_max}.mp3', 'rb')
    bot.send_audio(chat_id, audio)
    os.remove(f'{index_max}.mp3')


def update_pool_message(call, oper='add'):
    music_pool = ''
    if oper == 'sub':
        setup.start_idx -= setup.count_rows
    elif oper == 'add':
        setup.start_idx += setup.count_rows
    for idx, music in enumerate(
            setup.titles[(setup.current_page - 1) * setup.count_rows:setup.current_page * setup.count_rows]):
        music_pool += f'{setup.start_idx + idx}. {music}\n'
    bot.edit_message_text(music_pool, call.message.chat.id, call.message.message_id, reply_markup=gen_markup())


def pool_over():
    setup.make_default_setup()


@bot.message_handler(commands=['pool'])
def create_pool(message):
    ADMINS_ID = [admin.user.id for admin in bot.get_chat_administrators(message.chat.id)]
    if message.from_user.id in ADMINS_ID:
        music_pool = ''
        setup.links, setup.titles = get_links(setup.count_music)
        for idx, music in enumerate(
                setup.titles[(setup.current_page - 1) * setup.count_rows:setup.current_page * setup.count_rows]):
            music_pool += f'{setup.start_idx + idx}. {music}\n'
        bot.send_message(message.chat.id, music_pool, reply_markup=gen_markup())
    else:
        bot.send_message(message.chat.id, r"You don't have permission")


@bot.message_handler(commands=['finish'])
def finish_poll(message):
    receive_top_music(message.chat.id)
    pool_over()


@bot.message_handler(commands=['poptop'])
def pop_element_from_top(message):
    ADMINS_ID = [admin.user.id for admin in bot.get_chat_administrators(message.chat.id)]
    if message.from_user.id in ADMINS_ID:
        music_pool = ''
        setup.links, setup.titles = get_links(setup.count_music)
        for idx, music in enumerate(
                setup.titles[(setup.current_page - 1) * setup.count_rows:setup.current_page * setup.count_rows]):
            music_pool += f'{setup.start_idx + idx}. {music}\n'
        bot.send_message(message.chat.id, music_pool, reply_markup=gen_markup())
    else:
        bot.send_message(message.chat.id, r"You don't have permission")
