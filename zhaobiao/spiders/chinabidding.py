# -*- coding: utf-8 -*-
import re
from urllib import parse

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from datetime import datetime
from zhaobiao.items import ZhaobiaoItem
from zhaobiao.utils import clean_html, extract_phone, extract_name, login, get_keywords


class ChinabiddingSpider(CrawlSpider):
    name = 'chinabidding'
    allowed_domains = ['chinabidding.cn']

    keywords = get_keywords()

    start_urls = ['https://www.chinabidding.cn/search/searchzbw/search2?areaid=&keywords={}' \
                  '&page=1&categoryid=&rp=22&table_type=1000&b_date='.format(k) for k in keywords]
    rules = (
        Rule(LinkExtractor(allow=('search/searchzbw/search2',))),
        Rule(LinkExtractor(allow=('zbgg/.+\.html',)), callback='parse_item', process_request='add_cookie',
             follow=False),
    )

    def __init__(self, *args, **kwargs):
        super(ChinabiddingSpider, self).__init__(*args, **kwargs)
        self.cookies = self.login()


    def login(self):
        login_url = 'https://www.chinabidding.cn/cblcn/member.login/logincheck'
        data = {
            'name': '杭叉',
            'password': 'sesame88131983',
        }
        return login(login_url, data)

    def parse_item(self, response):
        item = ZhaobiaoItem()
        item['source'] = response.url
        item['addr'] = response.css('div.xiaob > div.fl.xiab_1 > a:nth-child(2)::text').extract_first()
        date_str = response.css('div.xiaob > div.fl.xiab_1 > span::text').extract_first()
        try:
            item['publish_date'] = datetime.strptime(date_str, '%Y-%m-%d')
        except Exception as e:
            self.log(e)

        refer = response.request.headers['Referer']
        refer = refer.decode('utf8')
        keywords = re.search(r'keywords=(.*?)&', refer).group(1)

        item['keyword'] = parse.unquote(keywords)

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

    def add_cookie(self, request):
        stats = self.crawler.stats
        stats.inc_value('pages_crawled')
        if stats.get_value('pages_crawled') % 60 == 0:
            self.cookies = self.login()
        request.cookies = self.cookies
        return request


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute("scrapy crawl chinabidding".split())
