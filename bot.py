import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, CommandHandler, Updater

from api import Api


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

api = Api('')


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="I'm a bot, <a href=\'http://google.com\'>please</a> talk to me!",
                     parse_mode='HTML')


def tags(bot, update):
    tag_list = api.get_tags()
    reply_markup = wrap_tags(tag_list)
    bot.send_message(chat_id=update.message.chat_id, text="Выберите интерсующие вас темы", reply_markup=reply_markup)


def wrap_tags(tags):
    return InlineKeyboardMarkup([[InlineKeyboardButton(tag, callback_data=tag)] for tag in tags])


REQUEST_KWARGS = {
    'proxy_url': 'socks5://178.62.60.220:1080',
    'urllib3_proxy_kwargs': {
        'username': 'proxy',
        'password': 'proxypassword',
    }
}


def edit_tags_message(bot, update):
    chat_id = update.callback_query.message.chat_id
    message_id = update.callback_query.message.message_id
    tag_list = api.get_absent_user_tags(chat_id)
    reply_markup = wrap_tags(tag_list)
    bot.edit_message_text(chat_id=chat_id,
                          message_id=message_id,
                          text="Выберите еще темы",
                          reply_markup=reply_markup)


def tags_callback(bot, update):
    tag = update.callback_query.data
    api.add_user_tag(update.callback_query.message.chat_id, tag)
    edit_tags_message(bot, update)


def start_bot(token):
    updater = Updater(token=token, request_kwargs=REQUEST_KWARGS)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    tags_handler = CommandHandler('tags', tags)
    dispatcher.add_handler(tags_handler)
    callback_query_handler = CallbackQueryHandler(tags_callback)
    dispatcher.add_handler(callback_query_handler)
    updater.start_polling()
    return updater.bot
