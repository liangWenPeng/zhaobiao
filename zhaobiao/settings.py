# -*- coding: utf-8 -*-

BOT_NAME = 'zhaobiao'

SPIDER_MODULES = ['zhaobiao.spiders']
NEWSPIDER_MODULE = 'zhaobiao.spiders'

ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS_PER_DOMAIN = 4
CONCURRENT_REQUESTS_PER_IP = 4

SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

EXTENSIONS = {
    'scrapy.contrib.closespider.CloseSpider': 300,
}

CLOSESPIDER_TIMEOUT = 60 * 60 * 5

# Override the default request headers:
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

# 网站搜索入口
START_SEARCH_URLS = {
    'a56products': 'http://www.56products.com/search/index.html?keyword={keyword}&ctrl=Trade',
    'a95306': 'http://wzcgzs.95306.cn/notice/indexlist.do?dealGroup=10&notTitle={keyword}',
    'chinabiddingcn': 'https://www.chinabidding.cn/search/searchzbw/search2?keywords={keyword}&table_type=1000&areaid=&categoryid=&b_date=',
    'chinabiddingcom': 'http://www.chinabidding.com/search/proj.htm',
    'zycg': 'http://www.zycg.gov.cn/article/article_search?keyword={keyword}&catalog='
}

# 网站登录地址
LOGIN_URLS = {
    'a56products': 'http://www.56products.com/login/index.html',
    'chinabiddingcn': 'https://www.chinabidding.cn/cblcn/member.login/logincheck',
}

# 网站登录账号
ACCOUNTS = {
    'a56products': [
        {
            'account': 'hzforklift',
            'pwd': 'sesame'
        },
    ],
    'chinabiddingcn': [
        {
            'name': '杭叉',
            'password': 'sesame88131983',
        },
    ],
}

NOT_LOGIN_STRS = {
    'a56products': '<p class="p-hide">请<a href="/login/index.html" style="color:#00F;">登录</a>查看信息</p>',
    'chinabiddingcn': '<td>招标编号：请 <a href="/cblcn/member.login/login?url=/zbgg/e8HIo.html" rel="nofollow">'
                      '登录</a> 查看</td>'
}

# 爬虫下载页面延迟（秒）
DOWNLOAD_DELAY = 15
DOWNLOAD_DELAYS = {
    'a56products': 120,
    'chinabiddingcn': 120,
}

# 每个域名的并发数
CONCURRENT_REQUESTS_PER_DOMAINS = {
    'a56products': 1,
    'chinabiddingcn': 1,
}
ITEM_PIPELINES = {
    'zhaobiao.pipelines.MongoPipeline': 300,
}

KEYWORDS_API = "http://123.56.24.201:9600/universe/hangcha/crawler/keywords"

# REDIS_HOST = 'localhost'
# REDIS_PORT = 6379

MONGO_URI = 'mongodb://10.23.169.125'
DB_USER = 'spider'
DB_PSW = 'lcworld'

LOG_LEVEL = 'INFO'

# 正则表达式部分
NAME_PREFIX = '联系人|联系人及联系方式|联系人及电话|联系方式|联系电话|联络人员|招标人员|负责人|采购人|联系方式|发布人|经办人|' \
              '招标人|技术咨询人|业务咨询|商务合作|技术'
NAME_TARGET = ['[\u4e00-\u9fa5]{2,4}']

TEL_PREFIX = '联系电话|联系方式|联系人电话|联络人电话|联系人及联系方式|电话|手机'
TEL_TARGET = r'\d{3,4}-\d{7,8}|\d{3,4}\s*-?\s*\d{7,8}|\(\d{3,4}\)\s*\d{7,8}|\d{7,8}|1[3,4,5,7,8]\d{9}'

ADDR_PREFIX = '采购中心地址|收货地点|送货地点|开标地点|办公地址|地址|地点'
ADDR_TARGET = ['[\u4e00-\u9fa5a-z0-9（）]{5,}?\s']

DEBUG = False

if DEBUG:
    SCHEDULER_FLUSH_ON_START = True
    MONGO_URI = 'mongodb://localhost'
    LOG_LEVEL = 'DEBUG'
