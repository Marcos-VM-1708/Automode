import googleapiclient.discovery


class Api:
    def __init__(self, key):
        self._key = key

    def build(self):
        api_service_name = "youtube"
        api_version = "v3"
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=self.key)
        return youtube

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key):
        self._key = key
