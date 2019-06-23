# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CosmeticsProduceLicenseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 详情id
    detail_id = scrapy.Field()
    # 企业名称
    company_name = scrapy.Field()
    # 许可证编号
    license_num = scrapy.Field()
    # 许可项目
    permit_item = scrapy.Field()
    # 企业住所
    address = scrapy.Field()
    # 生产地址
    produce_address = scrapy.Field()
    # 社会信用代码
    social_credit_code = scrapy.Field()
    # 法定代表人
    legal_person = scrapy.Field()
    # 企业负责人
    business_person = scrapy.Field()
    # 质量负责人
    quality_person = scrapy.Field()
    # 发证机关
    licensing_authority = scrapy.Field()
    # 签发人
    signer = scrapy.Field()
    # 日常监督管理机构
    daily_supervisory_authority = scrapy.Field()
    # 日常监督管理人员
    daily_supervisory_person = scrapy.Field()
    # 有效期至
    effective_date = scrapy.Field()
    # 发证日期
    issuance_date = scrapy.Field()
    # 状态
    state = scrapy.Field()  # 206 对应 正常
    crawl_time = scrapy.Field()
    pass
