# -*- coding: utf-8 -*-

BASE_URL = 'https://xueqiu.com'
LOGIN_URL = '/user/login'


BASE_HEADER = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36',
    'Origin': BASE_URL,
    'Referer': BASE_URL,
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Connection': 'keep-alive',
    'X-Requested-With': 'XMLHttpRequest',
}
