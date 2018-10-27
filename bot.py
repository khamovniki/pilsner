from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


def start(bot, update):
    print(update)
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


REQUEST_KWARGS={
    'proxy_url': 'socks5://178.62.60.220:1080',
    'urllib3_proxy_kwargs': {
        'username': 'proxy',
        'password': 'proxypassword',
    }
}
TOKEN = '462368299:AAGQZ-JKHzOOfNlwpMVf5g1LSAyLfWrqtxI'

updater = Updater(token=TOKEN, request_kwargs=REQUEST_KWARGS)
dispatcher = updater.dispatcher
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)


def start_bot():
    updater.start_polling()
