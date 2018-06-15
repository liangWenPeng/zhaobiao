# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhaobiaoItem(scrapy.Item):
    name = scrapy.Field()
    tel = scrapy.Field()
    addr = scrapy.Field()
    source = scrapy.Field()
    publish_date = scrapy.Field()
    crawled_date = scrapy.Field()
    title = scrapy.Field()
    keyword = scrapy.Field()

