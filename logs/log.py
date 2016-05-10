# coding: utf-8
import logging


logger = logging.getLogger("xueqiu")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

fh = logging.FileHandler('logs/.spider.log')
fh.setFormatter(formatter)
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setFormatter(formatter)
ch.setLevel(logging.INFO)

logger.addHandler(fh)
logger.addHandler(ch)
