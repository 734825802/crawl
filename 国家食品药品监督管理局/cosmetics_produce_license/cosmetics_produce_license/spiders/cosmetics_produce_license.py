# -*- coding: utf-8 -*-
import scrapy
import json
import time
from ..items import CosmeticsProduceLicenseItem


class CosmeticsProduceLicense(scrapy.Spider):
    name = 'cosmetics'
    allowed_domains = []
    start_urls = []

    # 初始，请求表单参数
    def start_requests(self):
        url = 'http://125.35.6.84:81/xk/itownet/portalAction.do?method=getXkzsList'
        for page in range(1, 330):
            form_data = {
                'on': 'true',
                'page': str(page),
                'pageSize': '15',
                'productName': '',
                'conditionType': '',
                'applyname': '',
                'applysn': ''
            }
            yield scrapy.FormRequest(
                url=url,
                formdata=form_data,
                callback=self.cosmetics_company_list,
            )
    # 化妆品公司列表信息
    def cosmetics_company_list(self, response):
        cosmetics_dict = json.loads(response.text)   # 获取化妆品公司列表
        for i in range(len(cosmetics_dict['list'])):    # 列表循环取出详情页ID
            detail_id = cosmetics_dict['list'][i]['ID']
            form_data = {
                'id': detail_id
            }
            yield scrapy.FormRequest(
                url='http://125.35.6.84:81/xk/itownet/portalAction.do?method=getXkzsById',
                formdata=form_data,
                meta={'detail_id': detail_id},
                callback=self.detail_cosmetics
            )

    # 化妆品生产许可证信息
    def detail_cosmetics(self, response):
        item = CosmeticsProduceLicenseItem()
        cosmetics_detail_dict = json.loads(response.text)  # 获取化妆品公司列表
        # 详情id
        item['detail_id'] = response.meta['detail_id']
        # 企业名称
        item['company_name'] = cosmetics_detail_dict['epsName']
        # 许可证编号
        item['license_num'] = cosmetics_detail_dict['productSn']
        # 许可项目
        item['permit_item'] = cosmetics_detail_dict['certStr']
        # 企业住所
        item['address'] = cosmetics_detail_dict['epsAddress']
        # 生产地址
        item['produce_address'] = cosmetics_detail_dict['epsProductAddress']
        # 社会信用代码
        item['social_credit_code'] = cosmetics_detail_dict['businessLicenseNumber']
        # 法定代表人
        item['legal_person'] = cosmetics_detail_dict['legalPerson']
        # 企业负责人
        item['business_person'] = cosmetics_detail_dict['businessPerson']
        # 质量负责人
        item['quality_person'] = cosmetics_detail_dict['qualityPerson']
        # 发证机关
        item['licensing_authority'] = cosmetics_detail_dict['qfManagerName']
        # 签发人
        item['signer'] = cosmetics_detail_dict['xkName']
        # 日常监督管理机构
        item['daily_supervisory_authority'] = cosmetics_detail_dict['rcManagerDepartName']
        # 日常监督管理人员
        item['daily_supervisory_person'] = cosmetics_detail_dict['rcManagerUser']
        # 有效期至
        item['effective_date'] = cosmetics_detail_dict['xkDate']
        # 发证日期
        item['issuance_date'] = cosmetics_detail_dict['xkDateStr']
        # 状态
        item['state'] = cosmetics_detail_dict['xkType']  # 206 对应 正常
        item['crawl_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        yield item
