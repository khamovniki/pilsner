from bot import start_bot
from server import run_server

TOKEN = '462368299:AAGQZ-JKHzOOfNlwpMVf5g1LSAyLfWrqtxI'

if __name__ == '__main__':
    bot = start_bot(TOKEN)
    run_server(bot)
