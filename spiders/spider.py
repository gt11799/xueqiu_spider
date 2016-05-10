# -*- coding: utf-8 -*-
import time
import pickle
import hashlib
import requests
from urlparse import urljoin

from config import USER_NAME, PASSWORD
from spiders.common import *
from logs.log import logger


class Spider(object):

    def __init__(self):
        self.session = requests.Session()

    def get_hash(self, string):
        m = hashlib.md5()
        m.update(string)
        return m.hexdigest()

    def login(self):
        url = urljoin(BASE_URL, LOGIN_URL)
        if self.check_login():
            logger.info('login already')
            return
        data = {
            'areacode': 86,
            'remember_me': 'on',
            'telephone': USER_NAME,
            'password': self.get_hash(PASSWORD),
        }
        response = self.session.post(url, headers=BASE_HEADER, data=data)
        logger.debug(response.content)
        if self.check_login():
            self.save_cookies()
        raise ValueError('login failed')

    def save_cookies(self):
        with open('spiders/.session', 'wb') as f:
            cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
            pickle.dump(cookies, f)

    def load_cookies(self):
        with open('spiders/.session') as f:
            return requests.utils.cookiejar_from_dict(pickle.load(f))

    def check_login(self):
        cookies = self.load_cookies()
        response = self.session.get(BASE_URL, headers=BASE_HEADER,
                                    cookies=cookies, allow_redirects=False)
        if response.status_code == 302:
            return True
        return False
