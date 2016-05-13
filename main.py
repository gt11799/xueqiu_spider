# -*- coding: utf-8 -*-

from spiders.spider import Spider
from spiders.html_parser import get_people, get_people_id


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


if __name__ == '__main__':
    crawl()
    # parse()
