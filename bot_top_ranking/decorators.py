def only_admins(func):
    def check_admin_permissions(message):
        bot = get_state.bot
        admins_id = [admin.user.id for admin in bot.get_chat_administrators(message.chat.id)]
        if message.from_user.id in admins_id:
            func(message)
        else:
            bot.send_message(message.chat.id, "You don't have permission")
    return check_admin_permissions


def get_state(state, bot):
    get_state.state = state
    get_state.bot = bot

    def next_decorator(func):
        return func
    return next_decorator


def started_pool(func):
    def check_is_pool_started(message):
        bot = get_state.bot
        state = get_state.state
        if not state.config["poll_started"]:
            bot.send_message(message.chat.id, "Poll hasn't started yet. Type /disco to start")
        else:
            func(message)
    return check_is_pool_started
