# -*- coding:utf-8 -*-
import time

from zhaobiao import utils
from zhaobiao.utils import get_keywords
from scrapy import Request
from scrapy_redis.spiders import RedisSpider
from zhaobiao.settings import START_SEARCH_URLS, LOGIN_URLS, ACCOUNTS, NOT_LOGIN_STRS, DOWNLOAD_DELAYS, \
    CONCURRENT_REQUESTS_PER_DOMAINS
import random


class ZbBaseSpider(RedisSpider):
    """
    招标爬虫基类
    """

    def __init__(self, *args, **kwargs):
        super(ZbBaseSpider, self).__init__(*args, **kwargs)
        self.search_url = START_SEARCH_URLS[self.name]
        self.keywords = get_keywords()
        self.login_url = LOGIN_URLS.get(self.name)
        self.accounts = ACCOUNTS.get(self.name)
        self.not_login_str = NOT_LOGIN_STRS.get(self.name)

        if self.login_url and self.accounts:
            self.cookie_updated = time.time()
            self.cookies = self.login()

        self.custom_settings = {}
        delay = DOWNLOAD_DELAYS.get(self.name)
        if delay:
            self.download_delay = delay
        current = CONCURRENT_REQUESTS_PER_DOMAINS.get(self.name)
        if current:
            self.concurrent_requests_per_domain = current

    def start_requests(self):
        for k in self.keywords:
            url = self.search_url.format(keyword=k)
            yield Request(url=url, meta={'keyword': k, 'is_start': True}, dont_filter=True)

    def login(self):
        data = random.choice(self.accounts)
        url = self.login_url
        self.logger.info('login {}'.format(data, url))
        cks = utils.login(url, data)
        self.cookie_updated = time.time()
        return cks

    def check_login_state(self, html, not_login_str=None):
        delay = self.download_delay or self.settings.get('DOWNLOAD_DELAY', 30)
        if time.time() - self.cookie_updated < delay * 5:  # 刚刚更新过cookies
            return True
        s = not_login_str or self.not_login_str
        if s and s in html:
            self.cookies = self.login()
            return False
        else:
            return True
