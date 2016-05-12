# -*- coding: utf-8 -*-
import time
import pickle
import hashlib
import requests
from urlparse import urljoin

from config import *
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
            logger.info('已经登录')
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
            logger.info('登录成功')
            self.save_cookies()
        raise ValueError('登录失败')

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

    def get_people(self):
        url = urljoin(BASE_URL, PEOPLE_URL)
        respond = self.session.get(url, headers=BASE_HEADER)
        with open('hh.html', 'w') as f:
            f.write(respond.content)
        logger.info('抓取')

    def get_people_detail(self, path):
        url = urljoin(BASE_URL, path)
        respond = self.session.get(url, headers=BASE_HEADER)
        with open('hhas.html', 'w') as f:
            f.write(respond.content)
        logger.info('抓取')

    def get_followers(self, uid):
        size = 100
        url = urljoin(BASE_URL, FOLLOWERS_URL)
        params = {
            'size': size,
            'pageNo': 1,
            'uid': uid,
            '_': int(time.time() * 1000)
        }
        respond = self.session.get(url, headers=FOLLOWER_HEADER, params=params)
        data = respond.json()
        max_page = data.get('maxPage')
        if not max_page:
            logger.error("获取粉丝失败")
            logger.error(data)
            raise ValueError("获取粉丝失败")
        result = data['followers']
        for page in range(1, max_page):
            time.sleep(FOLLOWER_PAGE_INTEVAL)
            params['pageNo'] = page
            params['_'] = int(time.time() * 1000)
            respond = self.session.get(url, headers=BASE_HEADER, params=params)
            data = respond.json()
            result += data['followers']
        return self.handle_followers(result)

    def handle_followers(self, data):
        return [(_['id'], _['screen_name']) for _ in data]
