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

def mock_upload_song(song,bot,state):
    with open('upload_song.txt','w+') as f:
        f.seek(0)
        f.truncate()
        f.write(song['author'] + ' | ' + song['title'])

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

def get_songs():
    songs = [
        {'title': 'Снова я напиваюсь', 'author': 'SLAVA MARLOW', 'link': 'https://zaycev.net/musicset/dl/177337abeb03fc429e45dfa2a4d61ac9/22485630.json', 'mark': 0, 'pos': 1, 'voted_users': []}, 
        {'title': 'Снова день, снова ночь', 'author': 'Dinar Rahmatullin', 'link': 'https://zaycev.net/musicset/dl/158c09c7a53581a9f0ea39cf8f0e6272/22438710.json', 'mark': 0, 'pos': 2, 'voted_users': []}, 
        {'title': 'Если тебе будет грустно', 'author': 'Niletto, Rauf & Faik', 'link': 'https://zaycev.net/musicset/dl/65f2858273af4c1747dcf013b4402a88/21847355.json', 'mark': 0, 'pos': 3, 'voted_users': []}, 
        {'title': 'KIDS', 'author': 'A4', 'link': 'https://zaycev.net/musicset/dl/a410d63e4eda19e55357aa0fd1fa3c9c/22446813.json', 'mark': 0, 'pos': 4, 'voted_users': []}, 
        {'title': 'El Problema', 'author': 'MORGENSHTERN & Тимати', 'link': 'https://zaycev.net/musicset/dl/9fe62e555d456555ed2c1147e5ae28bf/22357591.json', 'mark': 0, 'pos': 5, 'voted_users': []}, 
        {'title': 'Лада Приора [DJ MriD Remix]', 'author': 'Mr.NЁMA', 'link': 'https://zaycev.net/musicset/dl/2d55fa2e347759c16e4999dc9dc09cf6/22037001.json', 'mark': 0, 'pos': 6, 'voted_users': []}, 
        {'title': 'Ауф', 'author': 'Нурминский', 'link': 'https://zaycev.net/musicset/dl/9bc817a0041fd20e8a6b6d3e13bb84db/8633041.json', 'mark': 0, 'pos': 7, 'voted_users': []}, 
        {'title': 'Дико тусим', 'author': 'Даня Милохин, Николай Басков', 'link': 'https://zaycev.net/musicset/dl/538f6c8f022b658c22552ce82c586af8/22352471.json', 'mark': 0, 'pos': 8, 'voted_users': []}, 
        {'title': 'Чёрный Мерен', 'author': 'Navai', 'link': 'https://zaycev.net/musicset/dl/8ad100748d329d80cddbb90c71fb92f8/22446819.json', 'mark': 0, 'pos': 9, 'voted_users': []}, 
        {'title': 'Влад Бумага', 'author': 'Глент Кобяков', 'link': 'https://zaycev.net/musicset/dl/2c35498d6a56dc52e2bb6999ec306c2a/22031509.json', 'mark': 0, 'pos': 10, 'voted_users': []}, 
        {'title': 'Cadillac', 'author': 'MORGENSHTERN, Элджей', 'link': 'https://zaycev.net/musicset/dl/2848b9a36983769014bb81fa7615b074/17810114.json', 'mark': 0, 'pos': 11, 'voted_users': []}, 
        {'title': 'Гуччи флип флап', 'author': 'MNША, Lipuchka', 'link': 'https://zaycev.net/musicset/dl/7f260e40082360aa5c9ff6d4fbc6d244/22308605.json', 'mark': 0, 'pos': 12, 'voted_users': []}, 
        {'title': 'TIK TOK', 'author': 'Кобяков', 'link': 'https://zaycev.net/musicset/dl/0aeaab218ac966551820fbfbd358948c/22370264.json', 'mark': 0, 'pos': 13, 'voted_users': []}, 
        {'title': 'Ты такая красивая', 'author': 'Niletto', 'link': 'https://zaycev.net/musicset/dl/9c2c2dc0c5aebbcb0ed9c539ee614de7/17136308.json', 'mark': 0, 'pos': 14, 'voted_users': []}, 
        {'title': 'Юность', 'author': 'Dabro', 'link': 'https://zaycev.net/musicset/dl/03eeaa94c9a8593b35ae3ebf7d46b948/17991410.json', 'mark': 0, 'pos': 15, 'voted_users': []}, 
        {'title': 'Окей мы просто играем в жизнь', 'author': 'Тима Белорусских', 'link': 'https://zaycev.net/musicset/dl/e2e81a3be3152548bec28aac833a7013/21795525.json', 'mark': 0, 'pos': 16, 'voted_users': []},
        {'title': 'Поболело и прошло', 'author': 'HENSY', 'link': 'https://zaycev.net/musicset/dl/af098c4abe30e15f7b1312e2fab9682e/17695864.json', 'mark': 0, 'pos': 17, 'voted_users': []}, 
        {'title': 'А если это любовь?', 'author': 'HammAli & Navai', 'link': 'https://zaycev.net/musicset/dl/982af5f856a0ae7114b3d9d57d00d3fb/17897115.json', 'mark': 0, 'pos': 18, 'voted_users': []}, 
        {'title': 'Девчонка из сети', 'author': 'Вирус', 'link': 'https://zaycev.net/musicset/dl/e2dce0c53a28bdb8d2c85f0848c4272d/21658021.json', 'mark': 0, 'pos': 19, 'voted_users': []}, 
        {'title': 'РОЛЕКС', 'author': 'DAVA', 'link': 'https://zaycev.net/musicset/dl/1b0b67d99f6a9a5b0ee6bffb95593bfa/21655100.json', 'mark': 0, 'pos': 20, 'voted_users': []},
        {'title': 'Тишины хочу', 'author': 'Антиреспект', 'link': 'https://zaycev.net/musicset/dl/fc57ed25995a575009b81b944ed26370/3175360.json', 'mark': 0, 'pos': 21, 'voted_users': []}, 
        {'title': 'Lollipop', 'author': 'Gafur, JONY', 'link': 'https://zaycev.net/musicset/dl/4c1881ff11033b56f7e388c74c14d276/17977043.json', 'mark': 0, 'pos': 22, 'voted_users': []}, 
        {'title': 'Она любила розы', 'author': 'Ислам Итляшев', 'link': 'https://zaycev.net/musicset/dl/ef66d44cea7ff526823a9e47e37a4f78/21802740.json', 'mark': 0, 'pos': 23, 'voted_users': []}, 
        {'title': 'Fendi', 'author': 'Rakhim', 'link': 'https://zaycev.net/musicset/dl/a26d67abbd5119277e57b56990c7969b/18010379.json', 'mark': 0, 'pos': 24, 'voted_users': []}, 
        {'title': 'РАТАТАТАТА', 'author': 'MORGENSHTERN, Витя АК', 'link': 'https://zaycev.net/musicset/dl/5448561766eee1684e7af86a3b59cbcd/16877860.json', 'mark': 0, 'pos': 25, 'voted_users': []}
    ]
    return songs