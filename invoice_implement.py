# -*- coding: utf-8 -*-
import os
# gz： 即gzip。通常仅仅能压缩一个文件。与tar结合起来就能够实现先打包，再压缩。
# tar： linux系统下的打包工具。仅仅打包。不压缩
# tgz：即tar.gz。先用tar打包，然后再用gz压缩得到的文件
# zip： 不同于gzip。尽管使用相似的算法，能够打包压缩多个文件。只是分别压缩文件。压缩率低于tar。
# rar：打包压缩文件。最初用于DOS，基于window操作系统。
import gzip
import os
import tarfile
import zipfile
import rarfile
import pandas as pd
import pymongo
import logging


# 连接mongodb数据库
def connect_mongo_db():
    try:
        # 建立MongoDB数据库连接
        mondb_client = pymongo.MongoClient('192.168.4.210', 27017)
        # myclient = pymongo.MongoClient("mongodb://192.168.4.210:27017/")
        # mydb = myclient["invoice"]
        # # 用户验证
        # db = client.raw
        # db.authenticate("raw", "raw_bigdata963qaz")
        # 连接所用集合，也就是我们通常所说的表
        db = mondb_client.invoice
        invoice_info = db.invoice_info
        invoice_goods_info = db.invoice_goods_info
        return invoice_info, invoice_goods_info
    except Exception as e:
        logging.error(e)


# gz
# 因为gz一般仅仅压缩一个文件，全部常与其它打包工具一起工作。比方能够先用tar打包为XXX.tar,然后在压缩为XXX.tar.gz
# 解压gz，事实上就是读出当中的单一文件
def un_gz(file_name):
    """ungz zip file"""
    f_name = file_name.replace(".gz", "")
    # 获取文件的名称，去掉
    g_file = gzip.GzipFile(file_name)
    # 创建gzip对象
    open(f_name, "w+").write(g_file.read())
    # gzip对象用read()打开后，写入open()建立的文件里。
    g_file.close()
    # 关闭gzip对象


# tar
# XXX.tar.gz解压后得到XXX.tar，还要进一步解压出来。
# 注：tgz与tar.gz是同样的格式，老版本号DOS扩展名最多三个字符，故用tgz表示。
# 因为这里有多个文件，我们先读取全部文件名称。然后解压。例如以下：
# 注：tgz文件与tar文件同样的解压方法。
def un_tar(file_name):
    # untar zip file"""
    tar = tarfile.open(file_name)
    names = tar.getnames()
    if os.path.isdir(file_name + "_files"):
        pass
    else:
        os.mkdir(file_name + "_files")
    # 因为解压后是很多文件，预先建立同名目录
    for name in names:
        tar.extract(name, file_name + "_files/")
    tar.close()


# zip
# 与tar类似，先读取多个文件名称，然后解压。例如以下：
def un_zip(file_name):
    """unzip zip file"""
    zip_file = zipfile.ZipFile(file_name)
    if os.path.isdir(file_name + "_files"):
        pass
    else:
        os.mkdir(file_name + "_files")
    for names in zip_file.namelist():
        zip_file.extract(names, file_name + "_files/")
    zip_file.close()


# rar
# 由于rar通常为window下使用，须要额外的Python包rarfile。
# 可用地址： http://sourceforge.net/projects/rarfile.berlios/files/rarfile-2.4.tar.gz/download
# 解压到Python安装文件夹的/Scripts/文件夹下，在当前窗体打开命令行,
# 输入Python setup.py install
# 安装完毕。
def un_rar(file_name):
    """unrar zip file"""
    rar = rarfile.RarFile(file_name)  # 待解压文件
    if os.path.isdir(file_name + "_files"):
        pass
    else:
        os.mkdir(file_name + "_files")
    os.chdir(file_name + "_files")
    rar.extractall()  # 解压指定目录
    rar.close()


def un_zip_password(path, file_name):
    zf = zipfile.ZipFile(path + file_name)
    print(zf.namelist())
    for filename in zf.namelist():
        f = zf.open(filename, mode='r', pwd='123456'.encode('utf-8'))
        df_invoice_goods_info = pd.DataFrame(pd.read_excel(f, sheetname='发票信息'))
        f2 = zf.open(filename, mode='r', pwd='123456'.encode('utf-8'))
        df_invoice_info = pd.DataFrame(pd.read_excel(f2, sheetname='货物信息'))
        invoice_type = df_invoice_info.columns[0]  # 发票类型

        df_invoice_info_copy = df_invoice_info.copy()
        df_invoice_goods_info_copy = df_invoice_goods_info.copy()

        df_invoice_info_copy.columns = df_invoice_info.loc[0, :]
        df_invoice_goods_info_copy.columns = df_invoice_goods_info.loc[0, :]

        df_invoice_info_copy.drop(index=0, inplace=True)
        df_invoice_goods_info_copy.drop(index=0, inplace=True)

        df_invoice_info_copy.index = range(len(df_invoice_info_copy))
        df_invoice_goods_info_copy.index = range(len(df_invoice_goods_info_copy))

        df_invoice_goods_info_copy = df_invoice_goods_info_copy.rename(
            columns={'发票代码': 'invoice_code', '发票号码': 'invoice_no',
                     '税收分类编码': 'tax_classification_code', '货物或应税劳务名称': 'goods_taxable_sevices_name',
                     '规格型号': 'specification_model', '单位': 'unit',
                     '数量': 'number', '单价': 'unit_price',
                     '金额': 'amount', '税率': 'tax_rate', '税额': 'tax_amount'})

        df_invoice_info_copy = df_invoice_info_copy.rename(
            columns={'发票代码': 'invoice_code', '发票号码': 'invoice_no',
                     '开票日期': 'billing_date', '发票状态': 'invoice_state',
                     '销售方税号': 'seller_tax_no', '销售方名称': 'seller_name',
                     '购买方税号': 'buyer_tax_no', '购买方名称': 'buyer_name',
                     '金额': 'amount', '税额': 'tax_amount',
                     '价税合计': 'price_tax_total', '校验码': 'check_code',
                     '销售方地址电话': 'seller_address_phone', '销售方开户行及账号': 'seller_open_bank_account',
                     '购买方地址': 'buyer_address_phone', '购买方开户行及账号': 'buyer_open_bank_account',
                     '密码区': 'password_block', '备注': 'remarks',
                     '开票人': 'drawer', '收款人': 'payee', '复核人': 'checker'})

        for i in range(len(df_invoice_info_copy)):
            invoice_info_dict = df_invoice_info_copy.loc[
                i, ['invoice_code', 'invoice_no', 'billing_date', 'invoice_state',
                    'seller_tax_no', 'seller_name', 'buyer_tax_no', 'seller_name',
                    'amount', 'tax_amount', 'price_tax_total', 'check_code',
                    'seller_address_phone', 'seller_open_bank_account', 'buyer_address_phone',
                    'buyer_open_bank_account',
                    'password_block', 'remarks', 'drawer', 'payee', 'checker']].to_dict()

            invoice_goods_info_dict = df_invoice_goods_info_copy.loc[
                i, ['invoice_code', 'invoice_no', 'tax_classification_code', 'goods_taxable_sevices_name',
                    'specification_model', 'unit', 'number', 'unit_price', 'amount', 'tax_rate',
                    'tax_amount']].to_dict()

            invoice_info_dict['tax_classification_code'] = invoice_goods_info_dict['tax_classification_code']
            invoice_info_dict['goods_taxable_sevices_name'] = invoice_goods_info_dict['goods_taxable_sevices_name']
            invoice_info_dict['specification_model'] = invoice_goods_info_dict['specification_model']
            invoice_info_dict['unit'] = invoice_goods_info_dict['unit']
            invoice_info_dict['number'] = invoice_goods_info_dict['number']
            invoice_info_dict['unit_price'] = invoice_goods_info_dict['unit_price']
            invoice_info_dict['tax_rate'] = invoice_goods_info_dict['tax_rate']
            invoice_info_dict['invoice_type'] = invoice_type
            invoice_info.insert_one(invoice_info_dict)

    zf.close()


invoice_info, invoice_goods_info = connect_mongo_db()
test = "91360125MA38575J3Q-20200608162459099-202005-进项票-增值税普通发票 (1).zip"
path = 'C:/Users/Span/Downloads/'

for file in os.listdir(path):
    if file.endswith('.zip'):
        un_zip_password(path, file)

    # un_zip(inputname)
    # un_gz(inputname)
    # un_rar(inputname)
    # un_tar(inputname)
