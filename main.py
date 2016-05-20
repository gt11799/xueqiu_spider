# -*- coding: utf-8 -*-
import os
import sys
import time

from logs.log import logger
from config import *
from spiders.spider import Spider, if_int
from spiders.html_parser import get_people, get_people_id
from models.base import database, People, Chat


def crawl_people_info():
    spider = Spider()
    spider.visit_index()
    star_people = spider.get_people()
    for item in star_people:
        logger.info(u'开始抓取’%s‘的粉丝' % item[1])
        uid = item[0]
        if not if_int(uid):
            uid = spider.get_people_id(uid)
        if not uid:
            continue
        followers = spider.get_followers(uid)
        followers = [{'uid': _[0], 'user_name': _[1]} for _ in followers]
        with database.atomic():
            for idx in range(0, len(followers), 100):
                People.insert_many(followers[idx:idx + 100]).execute()
        logger.info(u'总共抓取了%s个粉丝' % len(followers))
        time.sleep(PER_STAR_FOLLOWER_INTEVAL)
    People.remove_duplicate()


def post(msg):
    spider = Spider()
    spider.visit_index()
    spider.login()
    spider.post(msg)


def send_chat_msg():
    spider = Spider()
    spider.login()
    chat_obj = Chat.get()
    logger.info(u'从id为%s的开始' % chat_obj.chatting_id)
    people = People.select().where(People.id > chat_obj.chatting_id)
    send_count = 0
    for person in people:
        result = spider.chat(person.uid, CHAT_MESSAGE)
        if not result:
            logger.error(u'发送给’%s‘失败' % person.user_name)
            time.sleep(PERCHAT_INTEVAL)
            continue
        send_count += 1
        logger.info(u'第%s条消息，发送给’%s‘成功' % (send_count, person.user_name))
        chat_obj.chatting_id = person.id
        chat_obj.save()
        time.sleep(PERCHAT_INTEVAL)


def remove_chat_history():
    chat_obj = Chat.get()
    chat_obj.chatting_id = 0
    chat_obj.save()
    logger.info(u'已经清空了发送历史')


def remove_login():
    Spider.clear_cookies()
    logger.info('登出完毕')


def remove_all_people():
    People.remove_all()
    logger.info('粉丝删除完毕')


def clear_log():
    os.remove('logs/.spider.log')
    logger.info('日志清除完毕')


def main(func, *args, **kwargs):
    funcs = {
        'crawl_people_info': crawl_people_info,
        'send_chat_msg': send_chat_msg,
        'remove_chat_history': remove_chat_history,
        'remove_login': remove_login,
        'remove_all_people': remove_all_people,
        'clear_log': clear_log,
        'post': post,
    }
    keys = funcs.keys()
    if func not in keys:
        raise ValueError("参数必须是一下几种: %s" % ', '.join(keys))
    funcs[func](*args, **kwargs)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise ValueError("请在main.py后面加上要执行的参数")
    func = sys.argv[1]
    kw = {}
    if func == "post":
        try:
            msg = sys.argv[2]
            kw = {"msg": msg}
        except IndexError:
            raise ValueError("MLGB 发消息不写正文你要搞毛啊")
    main(func, **kw)
