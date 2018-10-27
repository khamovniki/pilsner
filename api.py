import requests as r


class Api:
    def __init__(self, host):
        self.host = host

    def get_tags(self):
        return r.get(f'{self.host}/tags/list').json()

    def create_user(self, chat_id):
        r.post(f'{self.host}/create/{chat_id}')

    def add_user_tag(self, chat_id, tag):
        r.post(f'{self.host}/user/{chat_id}/addTag', json={"tag": tag})

    def get_absent_user_tags(self, chat_id):
        r.get(f'{self.host}/user/{chat_id}/listAbsentTags')
