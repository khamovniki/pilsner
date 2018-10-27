import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, CommandHandler, Updater

from api import Api


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

api = Api('http://localhost:8080/api')

REQUEST_KWARGS = {
    'proxy_url': 'socks5://178.62.60.220:1080',
    'urllib3_proxy_kwargs': {
        'username': 'proxy',
        'password': 'proxypassword',
    }
}


def start(bot, update):
    text = '''
<b>Привет!</b>
Этот бот присылает только те новости университета, которые вам интересны.
Выберите интересующие вас темы и мы будем делать рассылку, основываясь на ваших предпочтениях
'''
    bot.send_message(chat_id=update.message.chat_id,
                     text=text,
                     parse_mode='HTML')
    tags(bot, update)


def wrap_tags(tags):
    return InlineKeyboardMarkup([[InlineKeyboardButton(tag, callback_data=tag)] for tag in tags])


def tags(bot, update):
    tag_list = api.get_tags()
    reply_markup = wrap_tags(tag_list)
    bot.send_message(chat_id=update.message.chat_id, text="Выберите интерсующие вас темы", reply_markup=reply_markup)


def suggest_new_tags(bot, update, tag_list):
    chat_id = update.callback_query.message.chat_id
    message_id = update.callback_query.message.message_id
    reply_markup = wrap_tags(tag_list)
    text = '''
Выберите еще темы (либо проигнорируйте это сообщение, 
мы уже сохранили выбранные вами темы и будем делать рассылку по ним
'''
    bot.edit_message_text(chat_id=chat_id,
                          message_id=message_id,
                          text=text,
                          reply_markup=reply_markup)


def send_no_available_tags_message(bot, update):
    chat_id = update.callback_query.message.chat_id
    message_id = update.callback_query.message.message_id
    bot.edit_message_text(chat_id=chat_id,
                          message_id=message_id,
                          text='Вы выбрали все теги. А вас просто заинтересовать')


def edit_tags_message(bot, update):
    tag_list = api.get_absent_user_tags(update.callback_query.message.chat_id)
    if tag_list:
        suggest_new_tags(bot, update, tag_list)
    else:
        send_no_available_tags_message(bot, update)


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
