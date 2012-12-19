__all__ = ['config']

import threading
from version import VERSION

class Config(threading.local, object):

    def __init__(self):
        super(Config, self).__init__()
        self.api_key = None
        self.api_version = '1'
        self.base_url = 'https://api.postmaster.io'
        self._headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': 'Postmaster/%s (Python)' % VERSION,
        }

    @property
    def headers(self):
        if self.api_key:
            self._headers['Authorization'] = 'Basic %s' % ('%s:' % self.api_key).encode('base64').replace('\n','')
        return self._headers


config = Config()
