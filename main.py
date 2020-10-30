from bot.handlers import state, bot

if __name__ == "__main__":
    try:
        bot.polling(none_stop=True)
    except:
        pass
    finally:
        state.save_config()
