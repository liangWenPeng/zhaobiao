# -*- coding: utf-8 -*-
import logging
from datetime import datetime

from flask import jsonify, Flask, request
from flask.json import JSONEncoder
from pymongo import MongoClient

from zhaobiao.settings import DEBUG

logger = logging.getLogger(__name__)


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return obj.strftime('%Y-%m-%d %H:%M:%S')
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


class MongoDataQuery(object):
    def __init__(self, host=None, port=None, user=None, psw=None):
        if DEBUG:
            self.client = MongoClient(host=host, port=port, username=user, password=psw)
            self.coll = self.client['items']['ZhaobiaoItem']
        else:
            from zhaobiao.settings import MONGO_URI, DB_PSW, DB_USER
            self.client = MongoClient(MONGO_URI)
            self.db = self.client['items']
            self.db.authenticate(DB_USER, DB_PSW)
            self.coll = self.db['ZhaobiaoItem']

    def query_data(self, keyword, start_date=None, end_date=None, start=0, limit=20):

        # if not start_date:
        #     start_date = datetime.now() - timedelta(days=1)
        if not end_date:
            end_date = datetime.now()

        if start_date:
            query = {'crawled_date': {"$gte": start_date, "$lte": end_date}}
        else:
            query = {'crawled_date': {"$lte": end_date}}

        if keyword:
            query['keyword'] = keyword
        cursor = self.coll.find(query, {'_id': 0}).skip(start).limit(limit)
        logger.info(query)
        return list(cursor)

    def query_count(self, keyword, start_date=None, end_date=None):
        # if not start_date:
        #     start_date = datetime.now() - timedelta(days=1)
        if not end_date:
            end_date = datetime.now()

        if start_date:
            query = {'crawled_date': {"$gte": start_date, "$lte": end_date}}
        else:
            query = {'crawled_date': {"$lte": end_date}}

        if keyword:
            query['keyword'] = keyword
            logger.info(query)
        return self.coll.count(query=query)


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.json_encoder = CustomJSONEncoder


@app.route('/xiansuo')
def xiansuo():
    kw = request.args.get('keyword')
    start_date = request.args.get('start_date', type=int, default=0)
    end_date = request.args.get('end_date', type=int, default=0)
    try:
        if start_date:
            start_date = datetime.utcfromtimestamp(start_date/1000)
        if end_date:
            end_date = datetime.utcfromtimestamp(end_date/1000)
    except TypeError:
        pass
    except ValueError:
        result = {
            'state': 0,
            'msg': '日期格式错误'
        }
        return jsonify(result)
    start = request.args.get('start', type=int, default=0)
    limit = request.args.get('limit', type=int, default=20)
    try:
        data = app.db.query_data(kw, start_date, end_date, start, limit)
        result = {
            'state': 1,
            'data': data
        }
    except Exception as e:
        logger.warn(e)
        result = {
            'state': 0,
            'msg': e
        }
    return jsonify(result)


@app.route('/count')
def count():
    kw = request.args.get('keyword')
    start_date = request.args.get('start_date', type=int, default=0)
    end_date = request.args.get('end_date', type=int, default=0)
    try:
        if start_date:
            start_date = datetime.utcfromtimestamp(start_date/1000)
        if end_date:
            end_date = datetime.utcfromtimestamp(end_date/1000)
    except TypeError:
        pass
    except ValueError:
        result = {
            'state': 0,
            'msg': '日期格式错误'
        }
        return jsonify(result)
    try:
        data = app.db.query_count(kw, start_date, end_date)
        result = {
            'state': 1,
            'data': data
        }
    except Exception as e:
        logger.warn(e)
        result = {
            'state': 0,
            'msg': e
        }
    return jsonify(result)





if __name__ == '__main__':
    app.db = MongoDataQuery()
    if DEBUG:
        app.run(debug=True)
    else:
        from tornado.wsgi import WSGIContainer
        from tornado.httpserver import HTTPServer
        from tornado.ioloop import IOLoop

        http_server = HTTPServer(WSGIContainer(app))
        http_server.listen(80)  # 对应flask的端口
        IOLoop.instance().start()
