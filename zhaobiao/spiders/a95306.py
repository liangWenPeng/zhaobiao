# -*- coding:utf-8 -*-
import re
from datetime import datetime
from urllib import parse

from scrapy.spiders import Spider
from scrapy import Request
from zhaobiao.utils import *
from zhaobiao.items import ZhaobiaoItem


class A95306Spider(Spider):
    name = 'a95306'
    keywords = get_keywords()
    start_urls = ['http://wzcgzs.95306.cn/notice/indexlist.do?dealGroup=10&notTitle={}'.format(k) for k in keywords]

    def parse(self, response):
        keyword = re.search(r'notTitle=(.*)', response.url).group(1)
        keyword = parse.unquote(keyword)

        trs = response.css('tr')
        for tr in trs[1:]:
            item = ZhaobiaoItem()
            date_str = tr.css('td:nth-child(6)::text').extract_first()
            # date_str = re.search(r'\[(.*?)\]', date_str).group(1)
            if date_str:
                item['publish_date'] = datetime.strptime(date_str, '%Y-%m-%d')
            href = tr.css('td:nth-child(2) > a::attr(href)').extract_first()
            title = tr.css('td:nth-child(2) > a::text').extract_first()
            item['title'] = title
            item['keyword'] = keyword
            yield Request(response.urljoin(href), callback=self.parse_article, meta={'item': item}, priority=2)

        if 'extend' not in response.url:
            b = response.css('div.LsitInfoFrameBtmBg > b:nth-child(7)::text').extract_first()
            # print(b)
            page_num = int(re.search('共(\d+)页', b).group(1))
            if page_num > 1:
                for p in range(2, page_num + 1):
                    url = 'http://wzcgzs.95306.cn/notice/indexlist.do?dealGroup=10&unitType=&noticeType=&dealType=&materialType=&' \
                          'extend=1&curPage={}&notTitle={}&inforCode=&time0=&time1='.format(p, keyword)
                    yield Request(url=url, callback=self.parse)

    def parse_article(self, response):
        item = response.meta['item']
        item['source'] = response.url
        addr = response.css('div.noticeBox > div.topTlt > p.subhead > span:nth-child(6)::text').extract_first().strip()
        html = clean_html(response.text)
        item['addr'] = extract_addr(html, loose=False) or addr
        # tbody = response.css('body > table.detail_gg > tbody').extract_first()
        # print(tbody)
        div_center = clean_html(response.text)
        tel = extract_phone(div_center)
        if tel:
            item['tel'] = tel
        name = extract_name(div_center, loose=False)
        item['name'] = name or addr
        yield item


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute("scrapy crawl a95306".split())
