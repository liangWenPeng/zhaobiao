# -*- coding:utf-8 -*-
import re
from datetime import datetime
from urllib import parse

from scrapy.spiders import Spider
from scrapy import Request

from zhaobiao import utils
from zhaobiao.items import ZhaobiaoItem


class A56productsSpider(Spider):
    name = '56products'
    keywords = utils.get_keywords()
    start_urls = ['http://www.56products.com/search/index.html?keyword={}&ctrl=Trade'.format(k) for k in keywords]

    def __init__(self, *args, **kwargs):
        super(A56productsSpider, self).__init__(*args, **kwargs)
        self.cookies = self.login()

    def login(self):
        data = {
            'account':'hzforklift',
            'pwd':'sesame'
        }
        url = 'http://www.56products.com/login/index.html'
        return utils.login(url,data)


    def parse(self, response):
        lis = response.css('ul.lby-list > li')
        for li in lis[:-1]:
            item = ZhaobiaoItem()
            date_str = li.css('span::text').extract_first().strip()[1:-1]
            # date_str = re.search(r'\[(.*?)\]', date_str).group(1)
            item['publish_date'] = datetime.strptime(date_str, '%Y-%m-%d')
            href = li.css('a::attr(href)').extract_first()
            title = li.css('a::text').extract_first().strip()
            item['title'] = title

            keywords = re.search(r'keyword=(.*?)&', response.url).group(1)
            item['keyword'] = parse.unquote(keywords)
            yield Request(response.urljoin(href), callback=self.parse_article, meta={'item': item})

        next_page = response.css('a.next_page::attr(href)').extract_first()
        if next_page:
            yield Request(response.urljoin(next_page), callback=self.parse)

    def parse_article(self, response):
        item = response.meta['item']
        item['source'] = response.url
        # tbody = response.css('body > table.detail_gg > tbody').extract_first()
        # print(tbody)
        div_center = utils.clean_html(response.text)
        tel = extract_phone(div_center)
        if tel:
            item['tel'] = tel
        name = extract_name(div_center)
        if name:
            item['name'] = name
        yield item


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute("scrapy crawl 56products".split())