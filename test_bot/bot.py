import telebot
from telebot import types

bot = telebot.TeleBot('1389559561:AAGbQ0mIBnptbQ4-XCvqKLlNMN-szSIhyxI', parse_mode=None)

name = ''
surname = ''
age = 0


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.from_user.id, bot.get_me())
    bot.reply_to(message, message.text)


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/reg':
        print(message.from_user)
        bot.send_message(message.from_user.id, "Как тебя зовут?")
        bot.register_next_step_handler(message, get_name)  # следующий шаг – функция get_name
    else:
        bot.send_message(message.from_user.id, 'Напиши /reg')


def get_name(message):  # получаем фамилию
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия?')
    bot.register_next_step_handler(message, get_surname)


def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, 'Сколько тебе лет?')
    bot.register_next_step_handler(message, get_age)


def get_age(message):
    global age
    while age == 0:  # проверяем что возраст изменился
        try:
            age = int(message.text)  # проверяем, что возраст введен корректно
        except Exception:
            bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')  # кнопка «Да»
    keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    question = 'Тебе ' + str(age) + ' лет, тебя зовут ' + name + ' ' + surname + '?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


bot.polling(none_stop=True, interval=0)
