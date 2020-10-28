import os

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from work_music import download_music_link


def create_top(songs):
    top_list = sorted(songs, key=lambda song: song["mark"], reverse=True)
    return top_list


def upload_song(song, bot, state):
    song_name = f'{song["author"]} - {song["title"]}.mp3'
    download_music_link(song["link"], song_name)
    audio = open(song_name, 'rb')
    bot.send_audio(state.config["chatId"], audio)
    audio.close()
    os.remove(song_name)


def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Help", callback_data="help"),)
    return markup
