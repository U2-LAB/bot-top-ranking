import json
import os

from telebot import types
from telebot.apihelper import ApiTelegramException


def chat():
    return types.Chat(id=-1001349185527, type='supergroup')

def user(id=359862454,username='nikefr7'):
    # 843622237 - Kavahi
    return types.User(id=id, is_bot=False, first_name='Some User', username=username)

def message(user, chat, text='/start'):
    params = {'text': text}
    return types.Message(
        message_id=27891546, from_user=user, date=None, chat=chat, content_type='text', options=params, json_string=""
    )

def call(user,data,chat,message):
    return types.CallbackQuery(
        id=1,from_user=user,data=data,chat_instance=chat,message=message
    )

def mock_send_message(id,message_,parse_mode="HTML",reply_markup=None):
    with open('mock.txt','w+') as f:
        f.seek(0)
        f.truncate()
        print(message_,end='',file=f)
    return message(user(),chat())

def mock_pin_chat_message(state,message_id,disable_notification):
    pass

def mock_send_audio(chat_id,audio):
    with open('song.txt','w+') as f_song:
        f_song.seek(0)
        f_song.truncate()
        print('Audio',file=f_song,end='')

def get_capture(file_name='mock.txt'):
    with open(file_name, 'r+') as f:
        capture =''.join(f.readlines())
    os.remove(file_name)
    return capture

def mock_download_music_link(link,name):

    with open(f'{name}','wb+') as mp3_test:
        mp3_test.seek(0)
        mp3_test.truncate()
        mp3_test.write(b'Song in mp3')

def mock_state_init():
    pass

def mock_unpin_chat_message(chat_id):
    pass

def mock_promote_chat_member(id,user_id,can_delete_messages=True):
    if user_id == 666:
        result_json = {
            "error_code" : 444,
            "description" : 'descr'
        }
        raise ApiTelegramException('func','res',result_json)

def mock_set_chat_administrator_custom_title(chat_id,user_id,name):
    pass

