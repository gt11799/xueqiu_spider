# -*- coding: utf-8 -*-
import sys
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

reload(sys)
sys.setdefaultencoding('utf8')


class Spider(object):

    def __init__(self, user_name=None, password=None):
        self.session = requests.Session()
        self.uid = None
        self.user_name = user_name
        self.password = password

    def get_hash(self, string):
        m = hashlib.md5()
        m.update(string)
        return m.hexdigest()

    def _request(self, url, params={}):
        # 应该使用统一的request函数去请求，此处待重构
        try:
            response = self.session.get(url, headers=FOLLOWER_HEADER, params=params, timeout=10)
            return response
        except requests.ConnectionError, requests.ConnectTimeout:
            logger.error('%s请求超时')

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
            'username': self.user_name,
            'password': self.get_hash(self.password),
        }
        if if_int(self.user_name):
            data['telephone'] = data.pop('username')
        response = self.session.post(url, headers=BASE_HEADER, data=data)
        logger.debug(response.content)

        if self.check_login():
            logger.info('登录成功')
            self.get_people_id('8276760920')
            self.save_cookies()
            return
        raise ValueError('登录失败')

    def save_cookies(self):
        result = self.load_data()
        with open('spiders/.session', 'wb') as f:
            cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
            data = {
                'cookies': cookies,
                'uid': self.uid,
                'user_name': self.user_name,
            }
            result[self.user_name] = data
            pickle.dump(result, f)

    @classmethod
    def clear_cookies(cls):
        with open('spiders/.session', 'wb') as f:
            pickle.dump({}, f)

    def load_data(self):
        with open('spiders/.session') as f:
            try:
                return pickle.load(f)
            except EOFError:
                return {}

    def load_cookies(self):
        with open('spiders/.session') as f:
            try:
                data = pickle.load(f)
            except EOFError:
                return {}
            result = data.get(self.user_name)
            if not result:
                logger.info("账户未登录")
                return {}
            self.uid = result['uid']
            cookies = result['cookies']
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
        size = 1000
        url = urljoin(BASE_URL, FOLLOWERS_URL)
        params = {
            'size': size,
            'pageNo': 1,
            'uid': uid,
            '_': int(time.time() * 1000)
        }
        respond = self._request(url, params=params)
        if not respond:
            return []
        data = respond.json()
        max_page = data.get('maxPage')
        if not max_page:
            logger.error("获取粉丝失败")
            logger.error(data)
            raise ValueError("获取粉丝失败")
        result = data['followers']
        for page in range(1, max_page):
            time.sleep(FOLLOWER_PAGE_INTEVAL)
            logger.info('开始抓取第%s页的粉丝' % page)
            params['pageNo'] = page
            params['_'] = int(time.time() * 1000)
            respond = self._request(url, params=params)
            if not respond:
                continue
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
            'plain': msg,
            'to_group': False,
            'toId': uid,
            'sequenceId': sequenceId + 1
        }
        params = {'user_id': self.uid}
        cookies = self.load_cookies()
        respond = self.session.post(CHAT_URL, headers=CHAT_HEADER, cookies=cookies,
                                    params=params, data=json.dumps(data))
        if respond.status_code == 200:
            result = respond.json()
            error = result.get('error')
            if error:
                print '发送消息出错了'
                logger.debug(respond.content)
                raise ValueError(error.encode('utf8'))
            return True
        logger.debug(respond.status_code)
        logger.debug(respond.content)
        return False

    def post(self, msg, audience=[]):
        p = {"api": "/statuses/update.json", "_": int(time.time() * 1000)}
        cookie = self.load_cookies()
        url = urljoin(BASE_URL, TOKEN_URL)
        r = self.session.get(url, params=p, cookies=cookie,
                             headers=BASE_HEADER)
        try:
            token = r.json()['token']
        except (IndexError, TypeError, ValueError):
            logger.error("MLGB 出错了!")
            logger.error("\n%s\n", r.text)
            return
        audience = ' @'.join(audience)
        audience = ' @' + audience.strip()
        msg = '%s %s' % (msg, audience)
        logger.info('发送的内容是: %s' % msg)
        msg = msg.encode().decode()
        data = {"status": "<p>%s</p>" % msg, "session_token": token}
        url = urljoin(BASE_URL, POST_URL)
        r = self.session.post(url, data=data, cookies=cookie,
                              headers=BASE_HEADER)
        if r.status_code == 200:
            data = r.json()
            if not data.get('error_code') > -1:
                logger.debug("完事儿了.")
                return
        logger.error("MLGB 又出错了!")
        logger.error("\n%s\n", r.text)
        raise ValueError('发广播出错了')


def if_int(item):
    try:
        int(item)
    except ValueError:
        return False
    return True
