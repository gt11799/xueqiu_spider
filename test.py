# -*- coding: utf-8 -*-
import time

from logs.log import logger
from config import *
from spiders.spider import Spider
from spiders.html_parser import get_people, get_people_id
from models.base import database, People, Chat


def crawl():
    spider = Spider()
    spider.login()
    # spider.get_people()
    # spider.get_people_detail('5977514373')
    # print spider.get_followers('5977514373')
    print spider.chat(2862718994, '你好')


def parse():
    # f = open('hh.html')
    # get_people(f.read())
    f = open('hhas.html')
    get_people_id(f.read())


def if_int(item):
    try:
        int(item)
    except ValueError:
        return False
    return True


def test_model():
    People.insert_many([
        {"uid": 101010101011010, "user_name": 'dfadafdas'},
        {"uid": 101010101011010, "user_name": 'dfadafdas'}]).execute()


def crawl_people_info():
    spider = Spider()
    spider.visit_index()
    star_people = spider.get_people()
    for item in star_people:
        logger.debug(u'开始抓取’%s‘的粉丝' % item[1])
        uid = item[0]
        if not if_int(uid):
            uid = spider.get_people_id(uid)
        if not uid:
            continue
        followers = spider.get_followers(uid)
        print followers
        followers = [{'uid': _[0], 'user_name': _[1]} for _ in followers]
        print followers
        with database.atomic():
            for idx in range(0, len(followers), 100):
                People.insert_many(followers[idx:idx + 100]).execute()
        logger.debug('总共抓取了%s个粉丝' % len(followers))
        time.sleep(PER_STAR_FOLLOWER_INTEVAL)


def send_chat_msg():
    spider = Spider()
    spider.login()
    chat_obj = Chat().get()
    logger.debug('从%s开始' % chat_obj.chatting_id)
    people = People.select().where(People.id > chat_obj.chatting_id)
    send_count = 0
    for person in people:
        result = spider.chat(person.uid, CHAT_MESSAGE)
        if result:
            send_count += 1
            logger.debug('第%s消息，发送给’%s‘成功' % (send_count, person.user_name))
        chat_obj.chatting_id = person.uid
        chat_obj.save()
        time.sleep(PERCHAT_INTEVAL)


if __name__ == '__main__':
    crawl_people_info()
