# -*- coding: utf-8 -*-
import time
import json
import pickle
import hashlib
import requests
from urlparse import urljoin

from config import *
from spiders.common import *
from spiders.html_parser import *
from logs.log import logger


class Spider(object):

    def __init__(self):
        self.session = requests.Session()
        self.uid = None
        self.user_name = None

    def get_hash(self, string):
        m = hashlib.md5()
        m.update(string)
        return m.hexdigest()

    def visit_index(self):
        self.session.get(BASE_URL, headers=BASE_HEADER)

    def login(self):
        url = urljoin(BASE_URL, LOGIN_URL)
        if self.check_login():
            logger.info('已经登录')
            return
        data = {
            'areacode': 86,
            'remember_me': 'on',
            'username': USER_NAME,
            'password': self.get_hash(PASSWORD),
        }
        response = self.session.post(url, headers=BASE_HEADER, data=data)
        logger.debug(response.content)

        if self.check_login():
            logger.info('登录成功')
            self.get_people_id('8276760920')
            self.save_cookies()
            return
        raise ValueError('登录失败')

    def save_cookies(self):
        with open('spiders/.session', 'wb') as f:
            cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
            data = {
                'cookies': cookies,
                'uid': self.uid,
                'user_name': USER_NAME,
            }
            pickle.dump(data, f)

    @classmethod
    def clear_cookies(cls):
        with open('spiders/.session', 'wb') as f:
            pickle.dump({}, f)

    def load_cookies(self):
        with open('spiders/.session') as f:
            try:
                data = pickle.load(f)
            except EOFError:
                return {}
            self.user_name = data['user_name']
            if self.user_name != USER_NAME:
                logger.warning("账户变更，重新登录")
                self.uid = None
                return {}
            self.uid = data['uid']
            cookies = data['cookies']
            return cookies

    def check_login(self, load_cookie=True):
        if load_cookie:
            cookies = self.load_cookies()
            response = self.session.get(BASE_URL, headers=BASE_HEADER,
                                        cookies=cookies, allow_redirects=False)
        else:
            response = self.session.get(BASE_URL, headers=BASE_HEADER,
                                        allow_redirects=False)
        if response.status_code == 302:
            if self.uid is not None:
                return True
            location = response.headers['Location']
            uid = get_uid_from_url(location)
            if uid:
                self.uid = uid
                return True
            else:
                logger.error(u"从跳转链接解析uid出错了")
        return False

    def get_people(self):
        url = urljoin(BASE_URL, PEOPLE_URL)
        respond = self.session.get(url, headers=BASE_HEADER)
        result = get_people(respond.content)
        logger.info('抓取了%s个大V' % len(result))
        return result

    def get_people_id(self, path):
        url = urljoin(BASE_URL, path)
        respond = self.session.get(url, headers=BASE_HEADER)
        if respond.status_code == 200:
            uid = get_people_id(respond.content)
            return uid
        else:
            logger.error(u'抓取’%s‘用户的id失败' % path)

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

    def get_chat_sequence_id(self, uid):
        url = CHAT_HISTORY_URL % uid
        params = {
            'user_id': self.uid,
            'limit': 30,
            '_': int(time.time() * 1000)
        }
        cookies = self.load_cookies()
        respond = self.session.get(url, headers=CHAT_HEADER, params=params, cookies=cookies)
        if respond.status_code == 200:
            data = respond.json()
            if len(data) > 1:
                return data[-1]['sequenceId']
            else:
                return 96878141
        logger.error('获得聊天id失败')
        logger.error(respond.content)
        return False

    def chat(self, uid, msg):
        sequenceId = self.get_chat_sequence_id(uid)
        if not sequenceId:
            return False
        data = {
            'plain': CHAT_MESSAGE,
            'to_group': False,
            'toId': uid,
            'sequenceId': sequenceId + 1
        }
        params = {'user_id': self.uid}
        cookies = self.load_cookies()
        respond = self.session.post(CHAT_URL, headers=CHAT_HEADER, cookies=cookies,
                                    params=params, data=json.dumps(data))
        if respond.status_code == 200:
            return True
        logger.debug(respond.status_code)
        logger.debug(respond.content)
        return False
