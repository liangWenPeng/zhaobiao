# -*- coding:utf-8 -*-
import re
from datetime import datetime
from urllib import parse

from scrapy.spiders import Spider
from scrapy import Request, FormRequest
from zhaobiao.utils import *
from zhaobiao.items import ZhaobiaoItem
import math


class ChinabiddingcomSpider(Spider):
    name = 'chinabiddingcom'
    keywords = get_keywords()
    search_url = 'http://www.chinabidding.com/search/proj.htm'
    def start_requests(self):

        for k in self.keywords:
            data = {
                'fullText': k,
                'poClass': 'BidNotice',
            }
            yield FormRequest(url=self.search_url, formdata=data, meta={'keyword': k, 'is_start': True})

    def parse(self, response):
        lis = response.css('ul.as-pager-body > li')
        keyword = response.meta['keyword']
        for li in lis[:-1]:
            item = ZhaobiaoItem()
            date_str = li.css('span.time::text').extract_first().replace('发布时间：', '')
            item['publish_date'] = datetime.strptime(date_str, '%Y-%m-%d')
            href = li.css('a.as-pager-item::attr(href)').extract_first()
            # title = li.css('a.as-pager-item > h5 > span.txt::text').extract_first().strip()
            # item['title'] = title
            area = li.css('a.as-pager-item > div > dl > dd > span:nth-child(2) > strong::text').extract_first().strip()
            item['addr'] = area
            item['keyword'] = keyword
            yield Request(response.urljoin(href), callback=self.parse_article, meta={'item': item})
        if response.meta.get('is_start',False):
            item_num = response.css(
                '#lab-show > div.as-floor-normal > div.as-md > h3 > div > ul > li > span::text').extract_first()
            item_num = int(item_num)
            for page in range(2, math.ceil(item_num) + 1):
                data = {
                    'fullText': keyword,
                    'poClass': 'BidNotice',
                    'currentPage': str(page),
                    'infoClassCodes': '0105'
                }
                yield FormRequest(url=self.search_url, formdata=data, meta={'keyword': keyword})

    def parse_article(self, response):
        item = response.meta['item']
        item['source'] = response.url
        item['title'] = response.css('#lab-show > div.as-floor-normal > div.span-f > div > h3::text').extract_first()
        div_center = clean_html(response.text)
        addr = extract_addr(div_center)
        if addr:
            item['addr'] = addr
        tel = extract_phone(div_center)
        if tel:
            item['tel'] = tel
        name = extract_name(div_center)
        if name:
            item['name'] = name
        yield item


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute("scrapy crawl chinabiddingcom".split())
