# -*- coding: utf-8 -*-

BOT_NAME = 'zhaobiao'

SPIDER_MODULES = ['zhaobiao.spiders']
NEWSPIDER_MODULE = 'zhaobiao.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 30
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 4
CONCURRENT_REQUESTS_PER_IP = 4

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'zhaobiao.middlewares.ZhaobiaoSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'zhaobiao.middlewares.MyCustomDownloaderMiddleware': 543,
# }


ITEM_PIPELINES = {
    'zhaobiao.pipelines.MongoPipeline': 300,
}

KEYWORDS_API = "http://123.56.24.201:9600/universe/hangcha/crawler/keywords"

DB_USER = 'spider'
DB_PSW = 'lcworld'

DEBUG = True

if not DEBUG:
    MONGO_URI = 'mongodb://10.23.169.125'
    DB_USER = 'spider'
    DB_PSW = 'lcworld'
