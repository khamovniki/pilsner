from bottle import post, run, request, Bottle
from telegram import Bot


class Server(Bottle):
    def __init__(self, bot: Bot):
        super(Server, self).__init__()
        self.bot = bot
        self.post('/sendMessage', callback=self.send_message)

    def send_message(self):
        message = request.json
        print(message)
        msg_text = message['text']
        receivers = message['users']
        for user in receivers:
            self.bot.send_message(chat_id=user, text=msg_text)


def run_server(bot):
    server = Server(bot)
    server.run(host='localhost', port=8080)
