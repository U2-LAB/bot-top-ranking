import pytest
from bot_top_ranking.help_functions import upload_song
from bot_top_ranking.handlers import bot
from bot_top_ranking.config_class import State


@pytest.mark.smoke
def test_upload_song(set_temp_folder, capsys, mocker):
    mocker.patch.object(bot, 'send_audio', return_value=None)
    state = State(path_to_config=set_temp_folder)
    song = state.config["songs"][0]
    expected_output = ''
    upload_song(song, bot, state)
    out, err = capsys.readouterr()
    assert out == expected_output
