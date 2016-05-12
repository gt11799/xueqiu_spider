# -*- coding: utf-8 -*-

BASE_URL = 'https://xueqiu.com'
LOGIN_URL = '/user/login'
PEOPLE_URL = '/people'
FOLLOWERS_URL = '/friendships/followers.json'


BASE_HEADER = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36',
    'Host': 'xueqiu.com',
    'Origin': BASE_URL,
    'Referer': BASE_URL,
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Connection': 'keep-alive',
    'X-Requested-With': 'XMLHttpRequest',
}

FOLLOWER_HEADER = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36',
    'Host': 'xueqiu.com',
    'Connection': 'keep-alive',
    'cache-control': 'no-cache',
}
