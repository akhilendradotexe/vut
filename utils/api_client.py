import requests
from config.settings import BASE_URL


class APIClient:
    def __init__(self, base_url=None):
        self.base_url = base_url or BASE_URL
        self.session = requests.Session()

    def get(self, endpoint, **kwargs):
        return self.session.get(f"{self.base_url}{endpoint}", **kwargs)

    def post(self, endpoint, json=None, **kwargs):
        return self.session.post(f"{self.base_url}{endpoint}", json=json, **kwargs)

    def put(self, endpoint, json=None, **kwargs):
        return self.session.put(f"{self.base_url}{endpoint}", json=json, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self.session.delete(f"{self.base_url}{endpoint}", **kwargs)

    def patch(self, endpoint, json=None, **kwargs):
        return self.session.patch(f"{self.base_url}{endpoint}", json=json, **kwargs)
