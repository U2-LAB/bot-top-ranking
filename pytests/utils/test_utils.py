import os

import pytest
from telebot import types

from bot_top_ranking import help_functions
from bot_top_ranking.handlers import bot
from bot_top_ranking.config_class import State


@pytest.mark.smoke
def test_upload_song(set_temp_folder, capsys, mocker):
    mocker.patch.object(bot, 'send_audio', return_value=print("Song was uploaded", end=''))
    mocker.patch.object(help_functions, "_download_music_link", return_value=None)
    state = State(path_to_config=set_temp_folder)
    song = state.config["songs"][0]
    expected_output = "Song was uploaded"
    open(f'{song["author"]} - {song["title"]}.mp3', 'wb').close()
    help_functions.upload_song(song, bot, state)
    out, err = capsys.readouterr()
    assert out == expected_output


@pytest.mark.smoke
def test_create_top():
    songs = [
        {
            "title": "title",
            "author": "author",
            "link": 'https://zaycev.net/musicset/dl/65f2858273af4c1747dcf013b4402a88/21847355.json',
            "mark": 1,
            "pos": 1
        },
        {
            "title": "title",
            "author": "author",
            "link": 'https://zaycev.net/musicset/dl/65f2858273af4c1747dcf013b4402a88/21847355.json',
            "mark": 2,
            "pos": 1
        },
        {
            "title": "title",
            "author": "author",
            "link": 'https://zaycev.net/musicset/dl/65f2858273af4c1747dcf013b4402a88/21847355.json',
            "mark": 3,
            "pos": 1
        }
    ]
    assert help_functions.create_top(songs) == songs[::-1]


@pytest.mark.smoke
def test_gen_markup():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = 1
    keyboard.add(types.InlineKeyboardButton("Help", callback_data="help"),)
    assert help_functions.gen_markup().__dict__ == keyboard.__dict__


@pytest.mark.smoke
def test_download_music_link(set_temp_folder):
    link = 'https://zaycev.net/musicset/dl/65f2858273af4c1747dcf013b4402a88/21847355.json'
    file_name = set_temp_folder + "author - title.mp3"
    help_functions._download_music_link(link, file_name)
    print(os.getcwd())
    assert os.path.exists(file_name)
    os.remove(file_name)
