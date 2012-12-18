__all__ = ['config']

import threading
from version import VERSION

class Config(threading.local, object):

    def __init__(self):
        super(Config, self).__init__()
        self.api_key_secret = None
        self.api_version = '1'
        self.base_url = 'https://api.postmaster.io'
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': 'Postmaster/%s (Python)' % VERSION,
        }

config = Config()
