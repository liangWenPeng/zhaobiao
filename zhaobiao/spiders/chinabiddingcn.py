# -*- coding: utf-8 -*-

from datetime import datetime

from zhaobiao.items import ZhaobiaoItem
from zhaobiao.spiders.base import ZbBaseSpider
from zhaobiao.utils import clean_html, extract_phone, extract_name


class ChinabiddingcnSpider(ZbBaseSpider):
    """
    比联网爬虫 chinabidding.com.cn
    """
    name = 'chinabiddingcn'

    def parse(self, response):
        trs = response.css('#cTable > tbody > tr > td:nth-child(1) > table > tbody > tr > td > table > tbody > tr')
        keyword = response.meta['keyword']
        for tr in trs[1:-1]:
            href = tr.css('td:nth-child(2) > a::attr(href)').extract_first()
            yield Request(response.urljoin(href), callback=self.parse_article, meta={'keyword': keyword})

        next_page = response.css('#pages > span > a:nth-last-child(2)::attr(href)').extract_first()
        if next_page:
            yield Request(response.urljoin(next_page), callback=self.parse, dont_filter=True)

    def parse_article(self, response):
        if not self.check_login_state(response.text):
            return

        item = ZhaobiaoItem()
        item['source'] = response.url
        item['addr'] = response.css('div.xiaob > div.fl.xiab_1 > a:nth-child(2)::text').extract_first()
        date_str = response.css('div.xiaob > div.fl.xiab_1 > span::text').extract_first()
        try:
            item['publish_date'] = datetime.strptime(date_str, '%Y-%m-%d')
        except Exception as e:
            self.log(e)

        item['keyword'] = response.meta['keyword']

        div_center = clean_html(response.css('div.cen_xq').extract_first())
        tel = extract_phone(div_center)
        if tel:
            item['tel'] = tel
        name = extract_name(div_center)
        if name:
            item['name'] = name

        item['title'] = response.css('h1::text').extract_first()
        if item.get('tel') or item.get('name'):
            return item


if __name__ == '__main__':
    from scrapy import cmdline, Request

    cmdline.execute("scrapy crawl chinabiddingcn".split())
