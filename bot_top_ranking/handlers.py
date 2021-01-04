import re
from peewee import fn

from telebot.apihelper import ApiTelegramException

from bot_top_ranking.decorators import only_admins, started_pool
from bot_top_ranking.help_functions import gen_markup, upload_song, create_top
from bot_top_ranking.utils import bot, state
from bot_top_ranking.songs import Song


@bot.message_handler(commands=['help'])
def get_help(message):
    help_message = (
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
    bot.send_message(message.chat.id, help_message, parse_mode="HTML")


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    print(call.__dict__)
    if call.data == "help":
        get_help(call.message)


@bot.message_handler(commands=['disco'])
@only_admins
def create_poll(message):
    if state.config["poll_started"]:
        bot.send_message(message.chat.id, "Previous poll hasn't finished yet. Type /finish or use pined Message")
    else:
        state.config["poll_started"] = True
        state.config["chat_id"] = message.chat.id
        music_poll = ''
        for idx, song in enumerate(Song.select().order_by(Song.author).execute()):
            music_poll += f'{idx + 1}. {song.author} | {song.title}\n'
        poll = bot.send_message(state.config["chat_id"], music_poll, reply_markup=gen_markup())
        bot.pin_chat_message(state.config["chat_id"], poll.message_id, disable_notification=True)


@bot.message_handler(commands=['top'])
@started_pool
def get_songs_top_list(message):
    state.config["top_songs"].clear()
    create_top()
    music_poll = ''
    try:
        top_number = int(re.search(r'^/top ([\d]*)$', message.text).group(1))
        if top_number == 0:
            raise AttributeError
    except AttributeError:
        bot.send_message(message.chat.id, 'Incorrect input. Type /help to get information about commands')
    else:
        for idx, song in enumerate(state.config["top_songs"][:top_number]):
            music_poll += f'{idx + 1}. {song["author"]} | {song["title"]} | {song["mark"]} Votes\n'
        bot.send_message(message.chat.id, music_poll, reply_markup=gen_markup())


@bot.message_handler(commands=['vote'])
@started_pool
def vote_for_song(message):
    try:
        idx = int(re.search(r'^/vote ([\d]*)$', message.text).group(1))
        if idx > state.config["count_music"] or idx < 0:
            raise AttributeError
    except AttributeError:
        reply_message = f'Number should be less than {state.config["count_music"]} and greater than 0'
        bot.send_message(state.config["chat_id"], reply_message)
    else:
        state.config["top_songs"].clear()
        if str(message.from_user.id) not in Song.get_by_id(idx).voted_users:
            song_item = Song.get_by_id(idx)
            song_item.update(
                mark=song_item.mark + 1
                ).where(Song.id_music == song_item.id_music).execute()
            song_item.update(
                voted_users=fn.array_append(Song.voted_users, str(message.from_user.id))
                ).where(Song.id_music == song_item.id_music).execute()
        else:
            song_item = Song.get_by_id(idx)
            song_item.update(
                mark=song_item.mark - 1
                ).where(Song.id_music == song_item.id_music).execute()
            song_item.update(
                voted_users=fn.array_remove(Song.voted_users, str(message.from_user.id))
                ).where(Song.id_music == song_item.id_music).execute()


@bot.message_handler(commands=['poptop'])
@only_admins
@started_pool
def pop_element_from_top(message):
    try:
        if message.text == '/poptop' or message.text == '/poptop@DrakeChronoSilviumBot':
            idx = 0
        else:
            idx = int(re.search(r'^/poptop ([\d]*)$', message.text).group(1)) - 1
        if idx > state.config["count_music"] or idx < 0:
            raise AttributeError
    except AttributeError:
        reply_message = f'Number should be less than {state.config["count_music"]} and greater than 0'
        bot.send_message(state.config["chat_id"], reply_message)
    else:
        if not state.config["top_songs"]:
            create_top()
        song_item = state.config["top_songs"][idx]
        if state.config["upload_flag"]:
            upload_song(song_item, bot, state)
        else:
            bot_reply_message = f'{song_item["author"]} | {song_item["title"]}'
            bot.send_message(state.config["chat_id"], bot_reply_message)

        song_index = song_item["pos"]  # positions of songs starts by 1

        song_item = Song.get_by_id(song_index)
        Song.update(voted_users=[]).where(Song.id_music == song_item.id_music).execute()
        Song.update(mark=0).where(Song.id_music == song_item.id_music).execute()
        state.config["top_songs"] = []


@bot.message_handler(commands=['finish'])
@only_admins
@started_pool
def finish_poll(message):
    bot.unpin_chat_message(state.config["chat_id"])
    state.config["poll_started"] = False
    Song.truncate_table(restart_identity=True)
    state.save_config()
    state.__init__()
    bot.send_message(state.config["chat_id"], "Poll was finished")


@bot.message_handler(commands=['settings_mp3'])
@only_admins
def change_upload_flag(message):
    if message.text == '/settings_mp3' or message.text == '/settings_mp3@DrakeChronoSilviumBot':
        state.config["upload_flag"] = False if state.config["upload_flag"] else True
    else:
        switch = message.text.replace('/settings_mp3', '').split()[0]
        if switch == 'on':
            state.config["upload_flag"] = True
        elif switch == 'off':
            state.config["upload_flag"] = False
    bot_message = f'uploading songs is <b>{"Enabled" if state.config["upload_flag"] else "Disabled"}</b>'
    bot.send_message(state.config["chat_id"], bot_message, parse_mode="HTML")


@bot.message_handler(commands=['poll_status'])
@only_admins
def get_poll_status(message):
    status = (
        'Poll status\n'
        '———————————\n'
        f'Poll started: {state.config["poll_started"]}\n'
        f'Upload mp3: {"on" if state.config["upload_flag"] else "off"}'
    )
    bot.send_message(message.chat.id, status)


@bot.message_handler(commands=['setDJ'])
@only_admins
def set_dj_by_user_id(message):
    try:
        mentioned_user = re.search(r'^/setDJ @([\w]+)', message.text).group(1)
    except AttributeError:
        bot.send_message(message.chat.id, 'Incorrect input. Type /help to get information about commands')
    else:
        if mentioned_user not in state.config["users_for_promoting"]:
            state.config["users_for_promoting"].append(mentioned_user)
        bot.send_message(message.chat.id, f'@{mentioned_user} type /becomeDJ. It\'s privileges only for you ^_^')


@bot.message_handler(commands=['becomeDJ'])
def become_dj(message):
    if message.from_user.username not in state.config["users_for_promoting"]:
        bot.send_message(message.chat.id, "You cannot use this command")
    else:
        try:
            bot.promote_chat_member(message.chat.id, message.from_user.id, can_delete_messages=True)
            bot.set_chat_administrator_custom_title(message.chat.id, message.from_user.id, 'DJ')
            state.config["users_for_promoting"].pop(state.config["users_for_promoting"].index(message.from_user.username))
            bot.send_message(
                message.chat.id,
                f'@{message.from_user.username} You have been promoted to DJ. Congratulate 🏆🏆🏆'
            )
        except ApiTelegramException:
            reply_bot_message = 'You are admin. Why do you try to do it??? (╮°-°)╮┳━━┳ ( ╯°□°)╯ ┻━━┻'
            bot.send_message(message.chat.id, reply_bot_message)
