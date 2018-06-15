# -*- coding:utf-8 -*-
from scrapy.spiders import Spider
from zhaobiao.utils import get_keywords
from scrapy import Request


class ZbBaseSpider(Spider):
    keywords = get_keywords()

    def start_requests(self):
        for k in self.keywords:
            url = self.search_url.format(keyword=k)
            yield Request(url=url, meta={'keyword': k, 'is_start': True},dont_filter=True)
