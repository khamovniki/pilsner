import logging

from telegram.ext import CommandHandler, Filters, MessageHandler, Updater


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


def echo(bot, update):
    print(update.message.chat_id)
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


def tags(bot, update):
    pass


REQUEST_KWARGS = {
    'proxy_url': 'socks5://178.62.60.220:1080',
    'urllib3_proxy_kwargs': {
        'username': 'proxy',
        'password': 'proxypassword',
    }
}


def start_bot(token):
    updater = Updater(token=token, request_kwargs=REQUEST_KWARGS)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    echo_handler = MessageHandler(Filters.text, echo)
    dispatcher.add_handler(echo_handler)
    updater.start_polling()
    return updater.bot
