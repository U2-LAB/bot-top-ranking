import collections
import math
import os

import telebot
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

Song = collections.namedtuple('Song', ['link', 'title', 'mark', 'pos'])


class Setup:
    def __init__(self):
        self.make_default_setup()

    def make_default_setup(self):
        self.count_music = 6
        self.count_rows = 3
        self.current_page = 1
        links, titles = get_links(self.count_music)
        self.songs = [Song(link=links[idx], title=titles[idx], mark=0, pos=str(idx)) for idx in range(self.count_music)]
        self.voted_users = []
        self.current_idx = 1
        self.max_page = math.ceil(self.count_music / self.count_rows)
        self.pool_started = False
        self.message_id = None
        self.pool_id = None
        self.chat_id = None


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
            f'{get_emoji_number(setup.current_idx + idx)} - {setup.songs[setup.current_idx + idx - 1].mark}',
            callback_data=setup.songs[setup.current_idx + idx - 1].pos) for
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
    if not setup.pool_id:
        setup.pool_id = call.message.message_id
        setup.chat_id = call.message.chat.id
    if call.data == 'Next page':
        setup.current_page += 1
        update_pool_message(oper='add')
    elif call.data == 'Prev page':
        setup.current_page -= 1
        update_pool_message(oper='sub')
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
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=gen_markup())


@bot.message_handler(commands=['start'])
def get_start(message):
    bot.send_message(message.chat.id, r"Use /poll for starting poll of music")


@bot.message_handler(commands=['help'])
def get_help(message):
    bot.send_message(message.chat.id, r"Use /poll for starting poll of music")


def receive_top_music(chat_id):
    # if not setup.voted_users:
    #     bot.send_message(chat_id, "No one voted\nNext composition is")
    # else:
    #     max_element = max([(idx, song.mark) for idx, song in enumerate(setup.songs)], key=lambda song: song[1])
    #     index_max = max_element[0]
    #     bot.send_message(chat_id,
    #                      f"The winning composition is ... 🥁'Bam'🥁'Bam'🥁'Bam'🥁'Bam'")
    bot.send_message(chat_id, "Next composition is ...\n🥁'Bam'🥁'Bam'🥁'Bam'🥁'Bam'")
    setup.songs.sort(key=lambda song: song.mark)
    download_music_link(setup.songs[0].link)
    audio = open(f'{"song"}.mp3', 'rb')
    bot.send_audio(chat_id, audio)
    os.remove(f'{"song"}.mp3')


def update_pool_message(oper=None):
    music_pool = ''
    if oper == 'sub':
        setup.current_idx -= setup.count_rows
    elif oper == 'add':
        setup.current_idx += setup.count_rows
    for idx, song in enumerate(
            setup.songs[(setup.current_page - 1) * setup.count_rows:setup.current_page * setup.count_rows]):
        music_pool += f'{setup.current_idx + idx}. {song.title}\n'
    bot.edit_message_text(music_pool, setup.chat_id, setup.pool_id, reply_markup=gen_markup())


@bot.message_handler(commands=['poll'])
def create_pool(message):
    # COMMMMMEEEEEEENNNNNNTTTTTT
    # ADMINS_ID = [admin.user.id for admin in bot.get_chat_administrators(message.chat.id)]
    # if message.from_user.id in ADMINS_ID:
    if True:
        if setup.pool_started:
            markup = InlineKeyboardMarkup()
            btn_poll = InlineKeyboardButton(text='poll',url='https://vk.com')
            markup.add(btn_poll)
            bot.send_message(message.chat.id, "Previous poll ({}) hasn't finished yet. Type /finish",reply_markup=markup)
            return None
        setup.pool_started = True
        music_pool = ''
        for idx, song in enumerate(
                setup.songs[(setup.current_page - 1) * setup.count_rows:setup.current_page * setup.count_rows]):
            music_pool += f'{setup.current_idx + idx}. {song.title}\n'
        poll = bot.send_message(message.chat.id, music_pool, reply_markup=gen_markup())
        setup.message_id = poll.message_id
        setup.chat_id = poll.chat.id
        bot.pin_chat_message(setup.chat_id, setup.message_id)
    else:
        bot.send_message(message.chat.id, r"You don't have permission")


@bot.message_handler(commands=['finish'])  # Unnecessary command
def finish_poll(message):
    if setup.pool_started:
        receive_top_music(message.chat.id)
        bot.unpin_chat_message(setup.chat_id)
        setup.make_default_setup()
    else:
        bot.send_message(message.chat.id, "Pool hasn't started yet. Type /poll to start")


@bot.message_handler(commands=['top'])  # add regexp to extract number of songs
def get_songs_top_list(message):
    top_list = setup.songs.copy()
    top_list.sort(key=lambda song: song.mark, reverse=True)
    music_pool = ''
    for idx, song in enumerate(top_list[:5]):  # 5 - regexp
        music_pool += f'{idx + 1}. {song.title} Votes - {song.mark}\n'
    bot.send_message(message.chat.id, music_pool)


@bot.message_handler(commands=['poptop'])  # add regexp to extract number of songs
def pop_element_from_top(message):
    # ADMINS_ID = [admin.user.id for admin in bot.get_chat_administrators(message.chat.id)]
    # if message.from_user.id in ADMINS_ID:
    # COMMMMMEEEEEEENNNNNNTTTTTT
    if True:
        if setup.pool_started:
            idx = 0  # regexp
            is_changed = False
            # TODO update it
            top_list = setup.songs.copy()
            top_list.sort(key=lambda song: song.mark, reverse=True)
            download_music_link(top_list[idx].link)
            audio = open(f'{"song"}.mp3', 'rb')
            bot.send_audio(message.chat.id, audio)
            os.remove(f'{"song"}.mp3')
            # END
            for idx, vote in enumerate(setup.voted_users):
                if vote[1] == top_list[idx].pos:  # vote[1] = song position
                    setup.voted_users.pop(idx)
                    song_item = setup.songs[int(vote[1])]
                    setup.songs[int(vote[1])] = song_item._replace(mark=0)
                    is_changed = True
            if is_changed:
                bot.edit_message_reply_markup(setup.chat_id, setup.pool_id, reply_markup=gen_markup())
        else:
            bot.send_message(message.chat.id, "Pool hasn't started yet. Type /poll to start")
    else:
        bot.send_message(message.chat.id, r"You don't have permission")
