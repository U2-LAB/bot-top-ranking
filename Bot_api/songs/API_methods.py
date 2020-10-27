import requests

MAIN_URL = 'http://127.0.0.1:8000/'
HEADERS = {'Content-Type':'application/json'}
STATUS_CODE_OK = [200, 201, 204]

def add_chat(telegram_chat_id : int, polls=[]):
    chat_data = {
        "telegram_chat_id": telegram_chat_id,
        "polls": polls
    }
    r = requests.post(MAIN_URL+'api/chat/1',json=chat_data,headers=HEADERS)
    if r.status_code in STATUS_CODE_OK:
        print('OK - New chat was created')
    else:
        print('Error - ',r.status_code)

def update_chat(chat_id:int,telegram_chat_id:int,polls=[]):
    chat_data = {
        "telegram_chat_id": telegram_chat_id,
        "polls": polls
    }
    r = requests.put(MAIN_URL+f'api/chat/{chat_id}',json=chat_data,headers=HEADERS)
    if r.status_code in STATUS_CODE_OK:
        print('OK - chat was updated')
    else:
        print('Error - ',r.status_code)

def delete_chat(chat_id:int):
    r = requests.delete(MAIN_URL+f'api/chat/{chat_id}',headers=HEADERS)
    if r.status_code in STATUS_CODE_OK:
        print('OK - chat was deleted')
    else:
        print('Error - ',r.status_code)

def get_chat(chat_id=None)->dict:
    r = None
    if chat_id:
        r = requests.get(MAIN_URL+f'api/chat/{chat_id}')
    else:
        r = requests.get(MAIN_URL+'api/chat')
    if r.status_code in STATUS_CODE_OK:
        return r.json()
    else:
        return {}

def add_poll(poll_telegram_id:int,chat_id:int,songs=[]):
    poll_data = {
            "poll_telegram_id": poll_telegram_id,
            "chat_id": chat_id,
            "songs": songs
        }
    r = requests.post(MAIN_URL+'api/poll/1',json=poll_data,headers=HEADERS)
    if r.status_code in STATUS_CODE_OK:
        print('OK - New poll was created')
    else:
        print('Error - ',r.status_code)

def update_poll(poll_id:int,poll_telegram_id:int,chat_id:int,songs=[]):
    poll_data = {
            "poll_telegram_id": poll_telegram_id,
            "chat_id": chat_id,
            "songs": songs
        }
    r = requests.put(MAIN_URL+f'api/poll/{poll_id}',json=poll_data,headers=HEADERS)
    if r.status_code in STATUS_CODE_OK:
        print('OK - poll was updated')
    else:
        print('Error - ',r.status_code)

def delete_poll(poll_id:int):
    r = requests.delete(MAIN_URL+f'api/poll/{poll_id}',headers=HEADERS)
    if r.status_code in STATUS_CODE_OK:
        print('OK - poll was deleted')
    else:
        print('Error - ',r.status_code)

def get_poll(poll_id=None)->dict:
    r = None
    if poll_id:
        r = requests.get(MAIN_URL+f'api/poll/{poll_id}')
    else:
        r = requests.get(MAIN_URL+'api/poll')
    if r.status_code in STATUS_CODE_OK:
        return r.json()
    else:
        return {}

def add_song(poll_id:int,title:str,mark:int):
    song_data = {
        "poll_id": poll_id,
        "title": title,
        "mark": mark
    }
    r = requests.post(MAIN_URL+'api/song/1',json=song_data,headers=HEADERS)
    if r.status_code in STATUS_CODE_OK:
        print('OK - New song was created')
    else:
        print('Error - ',r.status_code)

def update_song(song_id:int,poll_id:int,title:str,mark:int):
    song_data = {
        "poll_id": poll_id,
        "title": title,
        "mark": mark
    }
    r = requests.put(MAIN_URL+f'api/song/{song_id}',json=song_data,headers=HEADERS)
    if r.status_code in STATUS_CODE_OK:
        print('OK - song was updated')
    else:
        print('Error - ',r.status_code)

def delete_song(song_id:int):
    r = requests.delete(MAIN_URL+f'api/song/{song_id}',headers=HEADERS)
    if r.status_code in STATUS_CODE_OK:
        print('OK - song was deleted')
    else:
        print('Error - ',r.status_code)

def get_song(song_id=None)->dict:
    r = None
    if song_id:
        r = requests.get(MAIN_URL+f'api/song/{song_id}')
    else:
        r = requests.get(MAIN_URL+'api/song')
    if r.status_code in STATUS_CODE_OK:
        return r.json()
    else:
        return {}

def update_song_mark(song_id:int,mark:int):
    song_data = {
        "mark": mark
    }
    r = requests.patch(MAIN_URL+f'api/song/{song_id}',json=song_data,headers=HEADERS)
    if r.status_code in STATUS_CODE_OK:
        print('OK - mark was updated')
    else:
        print('Error - ',r.status_code)