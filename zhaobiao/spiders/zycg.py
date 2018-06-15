# -*- coding:utf-8 -*-
import re
from datetime import datetime
from urllib import parse

from scrapy.spiders import Spider
from scrapy import Request
from zhaobiao.utils import *
from zhaobiao.items import ZhaobiaoItem


class ZycgSpider(Spider):
    name = 'zycg'
    keywords = get_keywords()
    start_urls = ['http://www.zycg.gov.cn/article/article_search?keyword={}&catalog='.format(k) for k in keywords]

    def parse(self, response):
        lis = response.css('ul.lby-list > li')
        keyword = re.search(r'keyword=(.*?)&', response.url).group(1)
        keyword = parse.unquote(keyword)
        for li in lis[:-1]:
            item = ZhaobiaoItem()
            date_str = li.css('span::text').extract_first().strip()[1:-1]
            # date_str = re.search(r'\[(.*?)\]', date_str).group(1)
            item['publish_date'] = datetime.strptime(date_str, '%Y-%m-%d')
            href = li.css('a::attr(href)').extract_first()
            title = li.css('a::text').extract_first().strip()
            item['title'] = title
            item['keyword'] = keyword
            yield Request(response.urljoin(href), callback=self.parse_article, meta={'item': item})

        next_page = response.css('a.next_page::attr(href)').extract_first()
        if next_page:
            yield Request(response.urljoin(next_page), callback=self.parse)

    def parse_article(self, response):
        item = response.meta['item']
        item['source'] = response.url
        # tbody = response.css('body > table.detail_gg > tbody').extract_first()
        # print(tbody)
        div_center = clean_html(response.text)
        tel = extract_phone(div_center)
        if tel:
            item['tel'] = tel
        name = extract_name(div_center)
        if name:
            item['name'] = name
        yield item


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute("scrapy crawl zycg".split())
