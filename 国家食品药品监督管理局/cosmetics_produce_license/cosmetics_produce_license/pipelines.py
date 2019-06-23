# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
import pymongo
from .items import CosmeticsProduceLicenseItem

class CosmeticsProduceLicensePipeline(object):
    def __init__(self):
        self.host = settings['MONGO_HOST']  # 获取配置中数据库地址
        self.port = settings['MONGO_PORT']  # 数据库端口
        self.dbName = settings['MONGO_DB']  # 数据库名
        self.user = settings['MONGODB_USER']  # 账号
        self.password = settings['MONGODB_PASSWORD']  # 密码
        self.client = pymongo.MongoClient(host=self.host, port=self.port)

        # 数据库登录需要账号密码的话
        self.client.raw.authenticate(self.user, self.password)
        tdb = self.client[self.dbName]
        self.coll = tdb[settings['MONGO_COLL']]

    def process_item(self, item, spider):
        if isinstance(item, CosmeticsProduceLicenseItem):
            cosmetics_produce_license_item = dict(item)
            if not self.coll.find_one({'license_num': cosmetics_produce_license_item['license_num']}):
                self.coll.insert(cosmetics_produce_license_item)
                return item
