# -*- coding:utf-8 -*-
import re
from datetime import datetime
from urllib import parse

from scrapy.spiders import Spider
from scrapy import Request

from zhaobiao import utils
from zhaobiao.items import ZhaobiaoItem
from zhaobiao.spiders.base import ZbBaseSpider


class A56productsSpider(ZbBaseSpider):
    name = 'a56products'
    search_url = 'http://www.56products.com/search/index.html?keyword={keyword}&ctrl=Trade'

    custom_settings = {
        'DOWNLOAD_DELAY': 60,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1
    }

    def __init__(self, *args, **kwargs):
        super(A56productsSpider, self).__init__(*args, **kwargs)
        self.cookies = self.login()

    def login(self):
        # print('login...')
        data = {
            'account': 'hzforklift',
            'pwd': 'sesame'
        }
        url = 'http://www.56products.com/login/index.html'
        return utils.login(url, data)

    def parse(self, response):
        lis = response.css('ul.bo-list-01 > li')
        for li in lis[:-1]:
            item = ZhaobiaoItem()
            date_str = li.css('div.bo-list-item-info > p:nth-child(1) > span > em::text').extract_first().strip()
            # date_str = re.search(r'\[(.*?)\]', date_str).group(1)
            item['publish_date'] = datetime.strptime(date_str, '%Y-%m-%d')
            href = li.css('div.bo-list-item-head > h3 > a::attr(href)').extract_first()
            keywords = re.search(r'keyword=(.*?)&', response.url).group(1)
            item['keyword'] = parse.unquote(keywords)
            yield Request(response.urljoin(href), callback=self.parse_article, meta={'item': item},
                          cookies=self.cookies)

        next_page = response.css('div.page > div > a.next::attr(href)').extract_first()
        if next_page:
            yield Request(response.urljoin(next_page), callback=self.parse,dont_filter=True)

    def parse_article(self, response):
        if not self.check_login_state(response.text):
            return
        item = response.meta['item']
        item['source'] = response.url
        item['title'] = response.css('div.con-areal > div > div > h2::text').extract_first()
        div_center = utils.clean_html(response.text)
        tel = utils.extract_phone(div_center)
        if tel:
            item['tel'] = tel
        name = utils.extract_name(div_center)
        if name:
            item['name'] = name
        item['addr'] = utils.extract_addr(div_center)
        return item

    def check_login_state(self, html):
        p = '<p class="p-hide">请<a href="/login/index.html" style="color:#00F;">登录</a>查看信息</p>'
        if p in html:
            self.login()
            return False
        else:
            return True


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute("scrapy crawl a56products".split())
