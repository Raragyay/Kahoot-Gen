import copy
from typing import Dict

import requests

from constants import DEFAULT_KAHOOT
from credentials import password, username


class KahootAPIConnection:
    def __init__(self):
        self.session: requests.Session = requests.session()
        self.login(username, password)

    def login(self, user: str, passwd: str):
        payload = {
            'grant_type': 'password',
            'password'  : passwd,
            'username'  : user
        }
        response = self.session.post("https://create.kahoot.it/rest/authenticate", json=payload)
        response_json = response.json()
        self.session.headers.update({
            'authorization': f'Bearer {response_json["access_token"]}'})
        self.user = response

    def load(self, kahoot_id: str):
        response = self.session.get(f'https://create.kahoot.it/rest/drafts/{kahoot_id}')
        if response.ok:
            response_json = response.json()
            return self.clean_metadata(response_json, False)

        response = self.session.get(f'https://create.kahoot.it/rest/kahoots/{kahoot_id}')
        if not response.ok:
            raise ValueError(f"Kahoot with uuid {kahoot_id} does not exist or is private.")
        new_kahoot = copy.deepcopy(DEFAULT_KAHOOT)
        new_kahoot['kahoot'] = response.json()
        new_kahoot['id'] = new_kahoot['kahoot']['uuid']
        new_kahoot['need_to_create_draft'] = True
        new_kahoot['kahootExists'] = True
        return new_kahoot

    def create_new(self, title=None):
        new_kahoot = copy.deepcopy(DEFAULT_KAHOOT)
        new_kahoot['title'] = title if title else new_kahoot['title']
        return self.create_draft(new_kahoot)

    def create_draft(self, kahoot):
        response = self.session.post(f"https://create.kahoot.it/rest/drafts", json=kahoot)
        return self.clean_metadata(response.json(), False)

    def update(self, kahoot):
        if kahoot['need_to_create_draft']:
            kahoot = self.create_draft(kahoot)
        response = self.session.put(f'https://create.kahoot.it/rest/drafts/{kahoot["kahoot"]["uuid"]}', json=kahoot)
        return self.clean_metadata(response.json(), False)

    def publish(self, kahoot):
        if kahoot['need_to_create_draft']:
            kahoot = self.update(kahoot)
        response = self.session.post(f'https://create.kahoot.it/rest/drafts/{kahoot["kahoot"]["uuid"]}/publish',
                                     json=kahoot)
        self.session.delete(f'https://create.kahoot.it/rest/kahoots/{kahoot["kahoot"]["uuid"]}/lock')
        response_json = response.json()
        response_json['need_to_create_draft'] = True
        return response

    @staticmethod
    def clean_metadata(kahoot: Dict, need_to_create_draft: bool):
        kahoot.pop('targetFolderId', None)
        kahoot.pop('type', None)
        kahoot.pop('created', None)
        kahoot.pop('modified', None)
        kahoot['need_to_create_draft'] = need_to_create_draft
        return kahoot
