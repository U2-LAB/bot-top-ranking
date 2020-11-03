from collections import namedtuple

import pytest
from telebot import types

from bot_top_ranking import decorators
from bot_top_ranking.config_class import State
from .conftest import bot

User = namedtuple('User', ['user'])
state = State()


@pytest.mark.smoke
def test_get_state(mocker, mock_message):
    mocker.patch.object(bot, "get_chat_administrators", return_valus=[])
    expected_result = ('state', 'bot')

    @decorators.get_state(*expected_result)
    def check_params():
        return decorators.get_state.state, decorators.get_state.bot

    assert check_params() == expected_result


@pytest.mark.decorator
def test_only_admin_decorator(mocker, mock_message, capsys):
    mocker.patch.object(bot, "get_chat_administrators", return_value=[User(types.User(1, None, 'Tester'))])
    expected_output = "only_admin_achieved"
    mock_message.from_user.id = 1

    @decorators.only_admins
    @decorators.get_state(state, bot)
    def check_is_admin(message):
        bot.send_message(0, expected_output)

    check_is_admin(mock_message)
    out, err = capsys.readouterr()
    assert out == expected_output


@pytest.mark.decorator
def test_only_admin_decorator_raises(mocker, mock_message, capsys):
    mocker.patch.object(bot, "get_chat_administrators", return_value=[])
    expected_output = "You don't have permission"

    @decorators.only_admins
    @decorators.get_state(state, bot)
    def stub(message):
        pass

    stub(mock_message)
    out, err = capsys.readouterr()
    assert out == expected_output


@pytest.mark.decorator
def test_started_pool_decorator(mock_message, capsys):
    expected_output = "started_pool_achieved"
    state.config["poll_started"] = True

    @decorators.started_pool
    @decorators.get_state(state, bot)
    def check_is_started(message):
        bot.send_message(0, expected_output)

    check_is_started(mock_message)
    out, err = capsys.readouterr()
    assert out == expected_output


@pytest.mark.decorator
def test_started_pool_decorator_raises(mock_message, capsys):
    expected_output = "Poll hasn't started yet. Type /disco to start"
    state.config["poll_started"] = False

    @decorators.started_pool
    @decorators.get_state(state, bot)
    def stub(message):
        pass

    stub(mock_message)
    out, err = capsys.readouterr()
    assert out == expected_output
