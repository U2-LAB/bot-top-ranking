import os

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_top(songs):
    top_list = sorted(songs, key=lambda song: song["mark"], reverse=True)
    return top_list


def _download_music_link(music_link, name):
    import requests
    ok_status_code = 200
    link = music_link
    req = requests.get(link, stream=True)
    if req.status_code == ok_status_code:
        with open(name, 'wb') as mp3:
            mp3.write(req.content)


def upload_song(song, bot, state):
    song_name = f'{song["author"]} - {song["title"]}.mp3'
    _download_music_link(song["link"], song_name)
    audio = open(song_name, 'rb')
    bot.send_audio(state.config["chat_id"], audio)
    audio.close()
    os.remove(song_name)


def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Help", callback_data="help"),)
    return markup
