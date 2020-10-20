import telebot
import os
import time

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from work_music import get_links, download_music_link

bot = telebot.TeleBot("1377360563:AAH4U7RFBVky5ttCrSMSTObEAFxOPOnNsDA", parse_mode=None)

CHAT_ID = None
COUNT_MUSIC = 5
MUSIC_POS = [str(pos) for pos in range(COUNT_MUSIC)]
MARKS = [0 for _ in range(COUNT_MUSIC)]
ADMINS_ID = [359862454]
VOTED_USERS = []
TIME_FOR_VOTE = 10 # in seconds


def gen_markup():
	markup = InlineKeyboardMarkup()
	markup.row_width = COUNT_MUSIC

	markup.add(
		InlineKeyboardButton(f'1️⃣ - {MARKS[0]}',callback_data=MUSIC_POS[0]),
		InlineKeyboardButton(f'2️⃣ - {MARKS[1]}',callback_data=MUSIC_POS[1]),
		InlineKeyboardButton(f'3️⃣ - {MARKS[2]}',callback_data=MUSIC_POS[2]),
		InlineKeyboardButton(f'4️⃣ - {MARKS[3]}',callback_data=MUSIC_POS[3]),
		InlineKeyboardButton(f'5️⃣ - {MARKS[4]}',callback_data=MUSIC_POS[4]),
	)
	return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
	
	if call.from_user.id not in VOTED_USERS:
		MARKS[int(call.data)]+=1
		bot.answer_callback_query(call.id, f"Answer is {call.data}")
		bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=gen_markup())
		VOTED_USERS.append(call.from_user.id)
	else:
		bot.answer_callback_query(call.id, f"You voted")

@bot.message_handler(commands=['start'])
def start(message):
	bot.send_message(message.chat.id, r"Use /pool for starting pool of music")

@bot.message_handler(commands=['help'])
def start(message):
	bot.send_message(message.chat.id, r"Use /pool for starting pool of music")

def receive_top_music(chat_id,links):
	index_max = 0
	if not VOTED_USERS:
		bot.send_message(chat_id, "No one voted\nLoading the first song")
	else:
		max_elem = max(MARKS)
		index_max = MARKS.index(max_elem)
		bot.send_message(chat_id,f"According to the results of voting, the winning composition is ... 🥁'Bam'🥁'Bam'🥁'Bam'🥁'Bam'")

	download_music_link(links[index_max],index_max)
	audio = open(f'{index_max}.mp3','rb')
	bot.send_audio(chat_id,audio)
	os.remove(f'{index_max}.mp3')

def pool_over():
	for index in range(COUNT_MUSIC):
		MARKS[index] = 0
		VOTED_USERS.clear()

@bot.message_handler(commands=['pool'])
def create_pool(message):
	if message.from_user.id in ADMINS_ID:
		links, titles = get_links(COUNT_MUSIC)
		music_pool = f"""
1. {titles[0]}
2. {titles[1]}
3. {titles[2]}
4. {titles[3]}
5. {titles[4]}
		"""
		bot.send_message(message.chat.id, music_pool, reply_markup=gen_markup())
		time.sleep(TIME_FOR_VOTE)
		receive_top_music(message.chat.id,links)
		pool_over()
	else:
		bot.send_message(message.chat.id, r"You don't have permission")