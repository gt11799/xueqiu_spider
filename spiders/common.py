# -*- coding: utf-8 -*-

BASE_URL = 'https://xueqiu.com'
LOGIN_URL = '/user/login'
PEOPLE_URL = '/people'
FOLLOWERS_URL = '/friendships/followers.json'
CHAT_HISTORY_URL = 'https://im3.xueqiu.com/im-comet/v2/sessions/%s-0/messages.json'
CHAT_URL = 'https://im3.xueqiu.com/im-comet/v2/messages.json'


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

CHAT_HEADER = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36',
    'Host': 'im5.xueqiu.com',
    'Origin': 'https://im5.xueqiu.com',
    'Connection': 'keep-alive',
    'cache-control': 'no-cache',
    'Content-Type': 'application/json'
}

COOKIE_SAMPLE = {
    'bid': '4bd9eb5737d5748ff5fc03f08d727219_io5147rv',
    'xq_a_token': 'de9a75ce8d374d969519333ddd2f46421524b83b',
    'xq_is_login': '1',
    'xq_r_token': '1e79b2de82bbfaf172468779b7dfa2d06a40f397',
    'xq_token_expire': 'Tue%20Jun%2007%202016%2009%3A12%3A16%20GMT%2B0800%20(CST)',
}
