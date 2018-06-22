# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo
from datetime import datetime

from scrapy.exceptions import DropItem


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db, is_debug, db_user, db_psw):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.is_debug = is_debug
        self.db_user = db_user
        self.db_psw = db_psw

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items'),
            is_debug=crawler.settings.get('DEBUG'),
            db_user=crawler.settings.get('DB_USER'),
            db_psw=crawler.settings.get('DB_PSW'),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        if not self.is_debug:
            self.db.authenticate(self.db_user, self.db_psw)

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if not item['tel'] and (not item['name'] or item['name'] == '中心'):
            raise DropItem('tel and name is required')

        collection_name = item.__class__.__name__
        coll = self.db[collection_name]

        if coll.find_one({'source': item['source']}):
            raise DropItem('item has existed in mongo')

        item['crawled_date'] = datetime.now()
        coll.insert(dict(item))
        return item
