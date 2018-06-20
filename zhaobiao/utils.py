# -*- coding:utf-8 -*-
import requests
import re
from zhaobiao.settings import KEYWORDS_API, DEBUG,NAME_PREFIX,NAME_TARGET,TEL_PREFIX,TEL_TARGET,ADDR_PREFIX,ADDR_TARGET
import logging

logger = logging.getLogger(__name__)


def cookie2dict(s):
    items = s.split(';')
    d = {t.split('=', 1)[0]: t.split('=', 1)[-1] for t in items if t}
    return d


def get_keywords():
    rsp = requests.get(KEYWORDS_API).json()
    if rsp['result'] == '0':
        logger.info('keywords:{}'.format(rsp['data']))
        return rsp['data']
    else:
        raise Exception('请求关键字失败:{}'.format(rsp['desc']))
        # return '叉车、牵引车、空箱堆高机、正面吊、堆垛机、搬运车、AVG'.split('、')


def re_search(pres, mids, targets, text, join_s=True):
    pat_base = r'{}\s*?{}\s*(?P<target>{})\s?'
    for p in pres:
        if join_s:
            p = r'\s*'.join(p)
        for m in mids:
            for target in targets:
                pat = pat_base.format(p, m, target)
                # print(pat)
                try:
                    target_text = re.search(pat, text)
                    if target_text:
                        result = target_text.group('target').strip()
                        logger.debug('{} {}'.format(pat,result))
                        return result
                except Exception as e:
                    print('Error', pat, e)


def clean_html(html):
    dr = re.compile(r'<[^>]+>', re.S)
    html = dr.sub(' ', html)
    html = html.replace('—', '-').replace('&nbsp;', ' ').replace(":", '：')

    html = re.sub(r'联\s*系\s*', '联系', html)
    html = re.sub(r'方\s*式\s*', '电话', html)
    html = re.sub(r'电\s*话\s*', '电话', html)
    html = re.sub(r'\s*-\s*', '-', html)
    html = re.sub(r'\+86-?', '', html)
    return html


def extract_phone(html, loose=True):
    pres = TEL_PREFIX.split('|')
    pres = [r'\s*'.join(p) for p in pres]
    mids = ['：', ':', ]
    mids = [r'{}\s*[\u4e00-\u9fa5]*?'.format(m) for m in mids]
    targets = TEL_TARGET.split('|')
    tel = re_search(pres, mids, targets, html, join_s=False)
    if not tel and loose:
        pres = '联系人|业务咨询|商务合作'.split('|')
        pres = [r'\s*'.join(p) for p in pres]
        pres = [r'{}.*?'.format(p) for p in pres]
        mids = ['：*', ':*', ' ', ]
        mids = [r'{}\s*[\u4e00-\u9fa5]*?'.format(m) for m in mids]
        tel = re_search(pres, mids, targets, html, join_s=False)
    return tel


def extract_name(html, loose=True):
    pres = NAME_PREFIX.split('|')
    mids = ['：', ':']
    mids = [r'{}\s*[0-9\-]*'.format(m) for m in mids]
    targets = NAME_TARGET
    name = re_search(pres, mids, targets, html)
    if loose and not name:
        name = re_search(pres, ['：*', ':*', ' '], targets, html)
    return name


def extract_addr(html, loose=True):
    pres = ADDR_PREFIX.split('|')
    mids = ['：', ':']
    targets = ADDR_TARGET
    addr = re_search(pres, mids, targets, html)
    if loose and not addr:
        addr = re_search(pres, ['：*', ':*', ' '], targets, html)
    return addr


def login(url, data):
    resp = requests.post(url=url, data=data, verify=False)
    return resp.cookies.get_dict()


if __name__ == '__main__':
    data = {
        'account': 'hzforklift',
        'pwd': 'sesame'
    }
    url = 'http://www.56products.com/login/index.html'
    ck = login(url, data)
    print(ck)
