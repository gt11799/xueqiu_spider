# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup


def get_people(content):
    '''
    `找人` 页面获得用户
    '''
    soup = BeautifulSoup(content)
    content = soup.find_all('div', 'box_topInfluence')
    content = content[0]
    print content.prettify()
    tags = content.find_all('a')
    result = []
    for tag in tags:
        name, href = tag.get('title'), tag.get('href')
        if name and href:
            result.append((tag['title'], tag['href']))
        else:
            print tag
    return result


def get_people_id(content):
    '''
    `个人详情` 获得用户id，针对部分用户的域名是个性域名
    '''
    uids = re.findall('var\suid\s=\s(\d+)?', content)
    if len(uids) > 0:
        return uids[0]
