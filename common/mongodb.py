#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:mongo.py
@time:2021/11/11
@email:tao.xu2008@outlook.com
@description:
"""
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import unittest

from loguru import logger as default_logger
from common.singleton import Singleton


class MongoDBOperation(object, metaclass=Singleton):
    """MongoDB数据库操作"""

    def __init__(self, db_host, db_port, db_user, db_password, db_name,
                 mechanism='SCRAM-SHA-1', show=False, logger=default_logger):
        self.db_host = db_host
        self.db_port = db_port
        self.db_user = db_user
        self.db_password = db_password
        self.db_name = db_name
        self.mechanism = mechanism
        self.show = show
        self.logger = logger

        self.conn = None
        self.database = None
        self.connect()

    def connect(self):
        """
        connect to MangoDB
        :return:
        """
        uri = "mongodb://%s:%s@%s:%s" % (self.db_user, self.db_password, self.db_host, self.db_port)
        self.logger.info("连接 {} ...".format(uri))
        self.conn = MongoClient(uri, authSource='admin', authMechanism=self.mechanism)
        try:
            self.conn.admin.command('ping')
            self.logger.info("MangoDB server available")
        except ConnectionFailure as e:
            self.logger.error("MangoDB server not available")
            raise e

        try:
            self.database = self.conn[self.db_name]
            self.logger.info("数据库: %s 连接成功！" % self.db_name)
        except Exception as e:
            raise e

    def close(self):
        self.logger.info("断开MangoDB数据库的连接...")
        self.conn.close()

    def read_table(self, table_name, query_filter=None, projection=None, limit=0):
        """
        读取目标表中数据
        :param table_name: 表名称
        :param query_filter: 查询条件 {}
        :param projection: 要读取字段清单 [] / {}, {"_id": False}
        :param limit: maximum number of results to return. A limit of 0 (the default) is equivalent to setting no limit
        :return:
        """
        self.logger.info("读取目标表:{}，query_filter:{}".format(table_name, query_filter))
        export_table = []
        try:
            table = self.database[table_name]
            for item in table.find(query_filter, projection, limit=limit):
                export_table.append(item)
            self.logger.info("MangoDB表：%s读取完毕，共读取%s行数据！" % (table_name, len(export_table)))
        except Exception as e:
            self.logger.error("查询失败或者数据库中无此表！数据表:{}，query_filter:{}".format(table_name, query_filter))
            raise e
        return export_table


class MongoDBTestCase(unittest.TestCase):
    """docstring for MongoDB"""

    def test_1(self):
        """测试读取表"""
        mdb = MongoDBOperation(db_host='47.96.184.58', db_port=7211, db_user='dustess', db_password='dustesssetsud',
                               db_name='yapi')
        tbs = mdb.read_table('interface', {'_id': 346216})
        print(tbs)


if __name__ == '__main__':
    # test
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(MongoDBTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
