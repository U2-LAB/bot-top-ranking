from bot_top_ranking.handlers import bot, state

if __name__ == "__main__":
    with state:
        bot.polling(none_stop=True)
