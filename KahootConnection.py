import copy

from credentials import username, password
import aiohttp
from constants import DEFAULT_KAHOOT


class KahootConnection:
    __instance = None
    initialized = False

    @staticmethod
    def get_instance():
        return KahootConnection.__instance

    @classmethod
    async def initialize(cls):
        cls.initialized = True
        instance = KahootConnection()
        cls.__instance = instance
        await instance.login(username, password)

    def __init__(self):
        if not KahootConnection.initialized:
            raise Exception("Please call KahootConnection.initialize() first")
        elif KahootConnection.__instance:
            raise Exception("Please call get_instance() instead of __init__")
        self.session = aiohttp.ClientSession()
        self.user = None

    async def login(self, user: str, passwd: str):
        payload = {
            'grant_type': 'password',
            'password': passwd,
            'username': user
        }
        response = await self.session.post("https://create.kahoot.it/rest/authenticate", json=payload)
        response_json = await response.json()
        await self.session.close()
        self.session = aiohttp.ClientSession(
            headers={'authorization': f'Bearer {response_json["access_token"]}'},
            raise_for_status=True
        )
        self.user = response

    async def load(self, kahoot_id: str):
        try:
            response = await self.session.get(f'https://create.kahoot.it/rest/drafts/{kahoot_id}')
            response_json = await response.json()
            return self.clean_metadata(response_json, False)
        except aiohttp.ClientResponseError:  # Not found in drafts
            pass
        try:
            response = await self.session.get(f'https://create.kahoot.it/rest/kahoots/{kahoot_id}')
            new_kahoot = copy.deepcopy(DEFAULT_KAHOOT)
            new_kahoot['kahoot'] = await response.json()
            new_kahoot['id'] = new_kahoot['kahoot']['uuid']
            new_kahoot['need_to_create_draft'] = True
            new_kahoot['kahootExists'] = True
            return new_kahoot
        except aiohttp.ClientResponseError:
            raise ValueError(f"Kahoot with uuid {kahoot_id} does not exist or is private.")

    async def create_new(self, title=None):
        new_kahoot = copy.deepcopy(DEFAULT_KAHOOT)
        new_kahoot['title'] = title if title else new_kahoot['title']
        return await self.create_draft(new_kahoot)

    async def create_draft(self, kahoot):
        response = await self.session.post(f"https://create.kahoot.it/rest/drafts", json=kahoot)
        return self.clean_metadata(await response.json(), False)

    async def update(self, kahoot):
        if kahoot['need_to_create_draft']:
            kahoot = await self.create_draft(kahoot)
        response = await self.session.put(f'https://create.kahoot.it/rest/drafts/{kahoot["kahoot"]["uuid"]}',
                                          json=kahoot)
        return self.clean_metadata(await response.json(), False)

    async def publish(self, kahoot):
        if kahoot['need_to_create_draft']:
            kahoot = await self.update(kahoot)
        response = await self.session.post(f'https://create.kahoot.it/rest/drafts/{kahoot["kahoot"]["uuid"]}/publish',
                                           json=kahoot)
        _ = await self.session.delete(f'https://create.kahoot.it/rest/kahoots/{kahoot["kahoot"]["uuid"]}/lock')
        response_json = await response.json()
        response_json['need_to_create_draft'] = True
        return response

    @staticmethod
    def clean_metadata(kahoot, need_to_create_draft):
        kahoot.pop('targetFolderId', None)
        kahoot.pop('type', None)
        kahoot.pop('created', None)
        kahoot.pop('modified', None)
        kahoot['need_to_create_draft'] = need_to_create_draft
