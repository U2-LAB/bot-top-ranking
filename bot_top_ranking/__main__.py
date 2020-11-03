from bot_top_ranking.handlers import bot
from bot_top_ranking.config_class import State

if __name__ == "__main__":
    with State():
        bot.polling(none_stop=True)
