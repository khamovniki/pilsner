from bottle import request, Bottle
from telegram import Bot


def prepare_msg(message):
    return '\n'.join(''.join(message.split('<p>')).split('</p>'))


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
            self.bot.send_message(chat_id=user, text=msg_text, parse_mode='HTML')


def run_server(bot):
    server = Server(bot)
    server.run(host='localhost', port=8090)
