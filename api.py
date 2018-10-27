import requests as r


class Api:
    def __init__(self, host):
        self.host = host

    def get_tags(self):
        return ['sport', 'quests', 'education']
        # return r.get(f'{self.host}/getTags').json()

    def create_user(self, chat_id):
        r.post(f'{self.host}/createUser/{chat_id}')

    def add_user_tag(self, chat_id, tag):
        pass
        # r.post(f'{self.host}/addTag/{chat_id}', json={"tag": tag})

    def get_absent_user_tags(self, chat_id):
        return ['sport', 'quests']
