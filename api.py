import requests as r


class Api:
    def __init__(self, host):
        self.host = host

    def create_user(self, chat_id):
        r.post(f'{self.host}/createUser/{chat_id}')

    def add_user_tag(self, chat_id, tag):
        r.post(f'{self.host}/addTag/{chat_id}', json={"tag": tag})
