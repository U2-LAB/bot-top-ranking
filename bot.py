import os
import re

import telebot
from dotenv import load_dotenv
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from config_class import State
from help_functions import upload_song, create_top, gen_markup
from work_music import download_music_link

load_dotenv()
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))
state = State()


# Decorators
def only_admins(func):
    def check_admin_permissions(message):
        admins_id = [admin.user.id for admin in bot.get_chat_administrators(message.chat.id)]
        if message.from_user.id in admins_id:
            func(message)
        else:
            bot.send_message(message.chat.id, "You don't have permission")
    return check_admin_permissions


def started_pool(func):
    def check_is_pool_started(message):
        if not state.config["pollStarted"]:
            bot.send_message(message.chat.id, "Poll hasn't started yet. Type /disco to start")
        else:
            func(message)
    return check_is_pool_started


@bot.message_handler(commands=['help'])
def get_help(message):
    help_message = (
        "<b>Admin commands</b>\n"
        "/disco to start poll\n"
        "/poptop [num] output referenced song (e.g. /poptop or /poptop 5)\n"
        "/finish to end poll\n"
        "/setDJ [mentioned user] set mentioned people a DJ (e.g. /setDJ @Admin)\n"
        "/settings_mp3 on|off\n"
        "/poll_status to print status of poll in this chat\n"
        "<b>User commands</b>\n"
        "/top [num] output top songs(e.g. /top 5)\n"
        "/vote [num] vote for song from poll (e.g. /vote 5)\n"
    )
    bot.send_message(message.chat.id, help_message, parse_mode="HTML")


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "help":
        get_help(call.message)


@bot.message_handler(commands=['disco'])
@only_admins
def create_poll(message):
    if state.config["pollStarted"]:
        bot.send_message(message.chat.id, "Previous poll hasn't finished yet. Type /finish or use pined Message")
    else:
        state.config["pollStarted"] = True
        state.config["chatId"] = message.chat.id
        music_poll = ''
        for idx, song in enumerate(state.config["songs"]):
            music_poll += f'{idx + 1}. {song["author"]} | {song["title"]}\n'
        poll = bot.send_message(state.config["chatId"], music_poll, reply_markup=gen_markup())
        bot.pin_chat_message(state.config["chatId"], poll.message_id, disable_notification=True)


@bot.message_handler(commands=['top'])
@started_pool
def get_songs_top_list(message):
    top_list = create_top(state.config["songs"])
    music_poll = ''
    try:
        top_number = int(re.search(r'^/top ([\d]*)$', message.text).group(1))
        if top_number == 0:
            raise AttributeError
    except AttributeError:
        bot.send_message(message.chat.id, 'Incorrect input type /help for information about commands')
    else:
        for idx, song in enumerate(top_list[:top_number]):
            music_poll += f'{idx + 1}. {song["author"]} | {song["title"]} | {song["mark"]} Votes\n'
        bot.send_message(message.chat.id, music_poll, reply_markup=gen_markup())


@bot.message_handler(commands=['vote'])
@started_pool
def vote_for_song(message):
    try:
        idx = int(re.search(r'^/vote ([\d]*)$', message.text).group(1)) - 1
    except AttributeError:
        bot.send_message(state.config["chatId"], '/help')
    else:
        if idx >= state.config["countMusic"] or idx < 0:
            bot.send_message(state.config["chatId"], f'Type {state.config["countMusic"]} > number > 0')
        elif message.from_user.id not in state.config["songs"][idx]["votedUsers"]:
            song_item = state.config["songs"][idx]
            song_item["mark"] += 1
            song_item["votedUsers"].append(message.from_user.id)
            state.config["songs"][idx] = song_item
        else:
            song_item = state.config["songs"][idx]
            song_item["mark"] -= 1
            song_item["votedUsers"].pop(song_item["votedUsers"].index(message.from_user.id))
            state.config["songs"][idx] = song_item


@bot.message_handler(commands=['poptop'])
@only_admins
@started_pool
def pop_element_from_top(message):
    try:
        if message.text == '/poptop':
            idx = 0
        else:
            idx = int(re.search(r'^/poptop ([\d]*)$', message.text).group(1)) - 1
    except AttributeError:
        bot.send_message(state.config["chatId"], 'Incorrect input')
    else:
        if idx > state.config["countMusic"]:
            bot.send_message(state.config["chatId"], f'Type {state.config["countMusic"]} < number')
        else:
            top_list = create_top(state.config["songs"])
            if state.config["uploadFlag"]:
                upload_song(top_list[idx], bot, state)
            else:
                bot_reply_message = f'{top_list[idx]["author"]} | {top_list[idx]["title"]}'
                bot.send_message(state.config["chatId"], bot_reply_message)
            song_index = top_list[idx]["pos"] - 1  # positions of songs starts by 1
            song_item = state.config["songs"][song_index]
            song_item["votedUsers"] = []
            song_item["mark"] = 0
            state.config["songs"][song_index] = song_item


@bot.message_handler(commands=['finish'])  # Unnecessary command
@only_admins
@started_pool
def finish_poll(message):
    bot.unpin_chat_message(state.config["chatId"])
    if os.path.exists(os.getenv("SAVED_JSON")):
        os.remove(os.getenv("SAVED_JSON"))
    state.__init__()


@bot.message_handler(commands=['settings_mp3'])
@only_admins
def change_upload_flag(message):
    if message.text == '/settings_mp3' or '/settings_mp3@DrakeChronoSilviumBot':
        state.config["uploadFlag"] = False if state.config["uploadFlag"] else True
    else:
        switch = message.text.replace('/settings_mp3', '').split()[0]
        if switch == 'on':
            state.config["uploadFlag"] = True
        elif switch == 'off':
            state.config["uploadFlag"] = False
    bot_message = f'uploading songs is <b>{"Enabled" if state.config["uploadFlag"] else "Disabled"}</b>'
    bot.send_message(state.config["chatId"], bot_message, parse_mode="HTML")


@bot.message_handler(commands=['poll_status'])
@only_admins
def get_poll_status(message):
    status = f'Poll status\n———————————\nPoll_started: {state.config["pollStarted"]}\nUpload mp3: \
{"on" if state.config["uploadFlag"] else "off"} '
    bot.send_message(state.config["chatId"], status)


@bot.message_handler(commands=['setDJ'])
def set_dj_by_user_id(message):
    try:
        mentioned_user = re.search(r'^/setDJ @([\w]*)', message.text).group(1)
    except AttributeError:
        bot.send_message(message.chat.id, '/help')
    else:
        state.config["usersForPromoting"].append(mentioned_user)
        bot.send_message(message.chat.id, f'@{mentioned_user} type /becomeDJ. It\'s privileges only for you ^_^')


@bot.message_handler(commands=['becomeDJ'])
def become_dj(message):
    if message.from_user.username in state.config["usersForPromoting"]:
        bot.promote_chat_member(message.chat.id, message.from_user.id, can_delete_messages=True)
        bot.set_chat_administrator_custom_title(message.chat.id, message.from_user.id, 'DJ')
        bot.send_message(
            message.chat.id,
            f'@{message.from_user.username} You have been promoted to DJ. Congratulate 🏆🏆🏆'
        )


if __name__ == "__main__":
    try:
        bot.polling(none_stop=True)
    except BaseException:
        pass
    finally:
        state.save_config()
