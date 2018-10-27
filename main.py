from bot import start_bot
from server import run_server

TOKEN = '732510087:AAGbb11R4Ugx8D7T0tI7hLB_KfhYUbU6nH8'

if __name__ == '__main__':
    bot = start_bot(TOKEN)
    run_server(bot)
