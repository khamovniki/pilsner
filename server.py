from bottle import request, Bottle
from telegram import Bot


def replace(string, target, replacement):
    return replacement.join(string.split(target))


def prepare_msg(message):
    return replace(replace(message, '<p>', ''), '</p>', '\n')


def remove_styles(message):
    no_strong = replace(replace(message, '<strong>', ''), '</strong>', '')
    no_italic = replace(replace(no_strong, '<em>', ''), '</em>', '')
    return no_italic

def failsafe(func):
    try:
        func()
    except:
        pass

class Server(Bottle):
    def __init__(self, bot: Bot):
        super(Server, self).__init__()
        self.bot = bot
        self.post('/bot/sendPost', callback=self.send_post)

    def send_post(self):
        message = request.json
        msg_text = prepare_msg(message['message'])
        receivers = message['users']
        for user in receivers:
            self.send_message(user, msg_text)

    def send_message(self, chat_id, message):
        try:
            failsafe(lambda: self.bot.send_message(chat_id=chat_id, text=message, parse_mode='HTML'))
        except:
            flatten_message = remove_styles(message)
            failsafe(lambda: self.bot.send_message(chat_id=chat_id, text=flatten_message, parse_mode='HTML'))


def run_server(bot):
    server = Server(bot)
    server.run(host='localhost', port=8090)
