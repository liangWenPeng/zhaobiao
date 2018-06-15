# -*- coding:utf-8 -*-
import requests
import re
from zhaobiao.settings import KEYWORDS_API, DEBUG


def cookie2dict(s):
    items = s.split(';')
    d = {t.split('=', 1)[0]: t.split('=', 1)[-1] for t in items if t}
    return d


def get_keywords():
    rsp = requests.get(KEYWORDS_API).json()
    if rsp['result'] == '0':
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
                        if DEBUG:
                            print(pat, result)
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
    tel_re = r'\d{3,4}-\d{7,8}|\d{3,4}\s*-?\s*\d{7,8}|\(\d{3,4}\)\s*\d{7,8}|\d{7,8}'
    phone_re = r'1[3,4,5,7,8]\d{9}'
    pres = '联系电话|联系方式|联系人电话|联络人电话|联系人及联系方式|电话|手机'.split('|')
    pres = [r'\s*'.join(p) for p in pres]
    mids = ['：', ':', ]
    mids = [r'{}\s*[\u4e00-\u9fa5]*?'.format(m) for m in mids]
    targets = '{}|{}'.format(phone_re, tel_re).split('|')
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
    pres = '联系人|联系人及联系方式|联系人及电话|联系方式|联系电话|联络人员|招标人员|负责人|采购人|联系方式|发布人|经办人|招标人|技术咨询人|' \
           '业务咨询|商务合作|技术'.split('|')
    mids = ['：', ':']
    mids = [r'{}\s*[0-9\-]*'.format(m) for m in mids]
    targets = ['[\u4e00-\u9fa5]{2,4}']
    name = re_search(pres, mids, targets, html)
    if loose and not name:
        name = re_search(pres, ['：*', ':*', ' '], targets, html)
    return name


def extract_addr(html, loose=True):
    pres = '采购中心地址|收货地点|送货地点|开标地点|办公地址|地址|地点'.split('|')
    mids = ['：', ':']
    targets = ['[\u4e00-\u9fa5a-z0-9（）]{5,}?\s']
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
    ck = login(url,data)
    print(ck)