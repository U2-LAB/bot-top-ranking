from collections import namedtuple

import pytest
import telebot

from bot_top_ranking import handlers
from bot_top_ranking import help_functions
from bot_top_ranking.utils import bot, state

DJ = namedtuple('DJ', ["promoting_users", "username", "expected_output"])

count_music = state.config["count_music"]
error_song_pos = (0, count_music + 1)
song_pos_to_try = (1, count_music // 2, count_music)
song_pos_ids = ['pos_{}'.format(pos) for pos in song_pos_to_try]
song_error_pos_idx = ['pos_{}'.format(pos) for pos in error_song_pos]


@pytest.mark.smoke
def test_callback_query(mock_call):
    handlers.callback_query(mock_call)


@pytest.mark.smoke
def test_get_help(mock_message, capsys):
    handlers.get_help(mock_message)
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
    out, err = capsys.readouterr()
    assert out == expected_output


@pytest.mark.smoke
def test_create_poll(mock_message, capsys, mocker):
    mocker.patch.object(telebot.TeleBot, "pin_chat_message", return_value='')
    state.config["poll_started"] = False
    expected_output = ''
    for idx, song in enumerate(state.config["songs"]):
        expected_output += f'{idx + 1}. {song["author"]} | {song["title"]}\n'
    handlers.create_poll(mock_message)
    assert state.config["poll_started"] is True
    out, err = capsys.readouterr()
    assert out == expected_output


@pytest.mark.smoke
def test_create_poll_raises(mock_message, capsys):
    state.config["poll_started"] = True
    expected_output = "Previous poll hasn't finished yet. Type /finish or use pined Message"
    handlers.create_poll(mock_message)
    out, err = capsys.readouterr()
    assert out == expected_output


@pytest.mark.smoke
@pytest.mark.voting
@pytest.mark.parametrize('song_pos', song_pos_to_try, ids=song_pos_ids)
def test_vote_for_song(mock_message, song_pos):
    state.config["poll_started"] = True
    mock_message.text = f"/vote {song_pos}"
    handlers.vote_for_song(mock_message)
    song_pos -= 1  # indexes starts by 0
    expected_mark = 1
    assert state.config["songs"][song_pos]["mark"] == expected_mark
    handlers.vote_for_song(mock_message)
    expected_mark_after_revoked = 0
    assert state.config["songs"][song_pos]["mark"] == expected_mark_after_revoked


@pytest.mark.voting
@pytest.mark.parametrize('song_pos', error_song_pos, ids=song_error_pos_idx)
def test_vote_for_song_raises(mock_message, song_pos, capsys):
    state.config["poll_started"] = True
    expected_output = "Number should be less than 25 and greater than 0"
    mock_message.text = f"/vote {song_pos}"
    handlers.vote_for_song(mock_message)
    out, err = capsys.readouterr()
    assert out == expected_output


@pytest.mark.smoke
@pytest.mark.parametrize('amount', (1, 5, 10, count_music + 10))
def test_get_songs_top_list(mock_message, capsys, amount):
    state.config["poll_started"] = True
    mock_message.text = f'/top {amount}'
    expected_output = ''
    top_list = help_functions.create_top(state.config["songs"])
    for idx, song in enumerate(top_list[:amount]):
        expected_output += f'{idx + 1}. {song["author"]} | {song["title"]} | {song["mark"]} Votes\n'
    handlers.get_songs_top_list(mock_message)
    out, err = capsys.readouterr()
    assert out == expected_output


@pytest.mark.smoke
@pytest.mark.parametrize('amount', (None, -15, 0))
def test_get_songs_top_list_raises(mock_message, capsys, amount):
    state.config["poll_started"] = True
    mock_message.text = f'/top {amount}'
    expected_output = 'Incorrect input. Type /help to get information about commands'
    handlers.get_songs_top_list(mock_message)
    out, err = capsys.readouterr()
    assert out == expected_output


@pytest.mark.smoke
@pytest.mark.popelem
@pytest.mark.parametrize('uploading', (True, False), ids=('uploading_enable', 'uploading_disable'))
@pytest.mark.parametrize('song_pos_from_top', song_pos_to_try + (None,), ids=song_pos_ids + ["without_pos", ])
def test_pop_element(mock_message, capsys, mocker, song_pos_from_top, uploading):
    mocker.patch.object(handlers, 'upload_song', return_value='')
    state.config["upload_flag"] = uploading
    state.config["poll_started"] = True
    if song_pos_from_top is None:
        mock_message.text = "/poptop"
        song_idx = 0
    else:
        mock_message.text = f"/poptop {song_pos_from_top}"
        song_idx = song_pos_from_top - 1
    song = state.config["songs"][song_idx]
    expected_output = '' if uploading else f'{song["author"]} | {song["title"]}'
    handlers.pop_element_from_top(mock_message)
    out, err = capsys.readouterr()
    assert out == expected_output


@pytest.mark.popelem
@pytest.mark.parametrize('song_pos_from_top', error_song_pos, ids=song_error_pos_idx)
def test_pop_element_from_top_raises(mock_message, capsys, song_pos_from_top):
    state.config["poll_started"] = True
    mock_message.text = f"/poptop {song_pos_from_top}"
    expected_output = f'Number should be less than {count_music} and greater than 0'
    handlers.pop_element_from_top(mock_message)
    out, err = capsys.readouterr()
    assert out == expected_output


@pytest.mark.smoke
def test_finish_poll(mock_message, capsys, mocker):
    mocker.patch.object(bot, 'unpin_chat_message', return_value=None)
    state.config["poll_started"] = True
    expected_output = "Poll was finished"
    handlers.finish_poll(mock_message)
    assert state.config["poll_started"] is False
    out, err = capsys.readouterr()
    assert out == expected_output


@pytest.mark.smoke
@pytest.mark.settings_mp3
def test_change_upload_flag(mock_message, capsys):
    current_upload_flag = state.config["upload_flag"]
    mock_message.text = "/settings_mp3"
    handlers.change_upload_flag(mock_message)
    assert state.config["upload_flag"] != current_upload_flag
    expected_output = f'uploading songs is <b>{"Enabled" if state.config["upload_flag"] else "Disabled"}</b>'
    out, err = capsys.readouterr()
    assert out == expected_output


@pytest.mark.smoke
@pytest.mark.settings_mp3
@pytest.mark.parametrize('switch', ('on', 'off'), ids=('on', 'off'))
def test_change_upload_flag_by_switch(mock_message, capsys, switch):
    state.config["upload_flag"] = False if switch == 'on' else True
    expected_flag = True if switch == 'on' else False
    mock_message.text = f"/settings_mp3 {switch}"
    handlers.change_upload_flag(mock_message)
    expected_output = f'uploading songs is <b>{"Enabled" if state.config["upload_flag"] else "Disabled"}</b>'
    assert state.config["upload_flag"] == expected_flag
    out, err = capsys.readouterr()
    assert out == expected_output


@pytest.mark.smoke
def test_get_poll_status(mock_message, capsys):
    expected_output = (
        'Poll status\n'
        '———————————\n'
        f'Poll started: {state.config["poll_started"]}\n'
        f'Upload mp3: {"on" if state.config["upload_flag"] else "off"}'
    )
    handlers.get_poll_status(mock_message)
    out, err = capsys.readouterr()
    assert out == expected_output


@pytest.mark.work_with_dj
def test_set_dj_by_user_id(mock_message, capsys):
    mock_message.text = "/setDJ @Admin"
    expected_output = f'@Admin type /becomeDJ. It\'s privileges only for you ^_^'
    handlers.set_dj_by_user_id(mock_message)
    assert len(state.config["users_for_promoting"]) > 0 and 'Admin' in state.config["users_for_promoting"]
    out, err = capsys.readouterr()
    assert out == expected_output


@pytest.mark.work_with_dj
@pytest.mark.parametrize('gibberish', ('#lorum', 'ipsum', '@'))
def test_set_dj_by_user_id_raises(mock_message, capsys, gibberish):
    mock_message.text = f"/setDJ {gibberish}"
    expected_output = "Incorrect input. Type /help to get information about commands"
    handlers.set_dj_by_user_id(mock_message)
    out, err = capsys.readouterr()
    assert out == expected_output


@pytest.mark.work_with_dj
@pytest.mark.parametrize('users', [
    pytest.param(DJ([], 'Vasya', "You cannot use this command"), id='empty_list'),
    pytest.param(DJ(
        [bot.get_me().username],
        bot.get_me().username,
        'You are admin. Why do you try to do it??? (╮°-°)╮┳━━┳ ( ╯°□°)╯ ┻━━┻'),
        id='admin_user'),
    pytest.param(DJ(
        ['test_username'],
        'test_username',
        '@test_username You have been promoted to DJ. Congratulate 🏆🏆🏆'),
        id='promoted_user')
])
def test_become_dj(mock_message, capsys, mocker, users):
    mock_message.from_user.username = users.username
    state.config["users_for_promoting"] = users.promoting_users
    if users.username in users.promoting_users and users.username != bot.get_me().username:
        mocker.patch.object(bot, "promote_chat_member", return_value=None)
        mocker.patch.object(bot, "set_chat_administrator_custom_title", return_value=None)
    handlers.become_dj(mock_message)
    out, err = capsys.readouterr()
    assert out == users.expected_output
