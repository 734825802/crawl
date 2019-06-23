# -*- coding: utf-8 -*-

# Scrapy settings for cosmetics_produce_license project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'cosmetics_produce_license'

SPIDER_MODULES = ['cosmetics_produce_license.spiders']
NEWSPIDER_MODULE = 'cosmetics_produce_license.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

#-----------------------------------------------------------------------------------------------------------
#在使用scrapy抓取数据的时候使用了代理IP，难免会遇到代理IP失效的情况。
# 因为对数据完整性要求较高，请问如何设置只要没有成功的返回response则把任务重新放进Request队列中去继续爬取？
#-----------------------------------------------------------------------------------------------------------

#是否开启retry
RETRY_ENABLED= True
RETRY_HTTP_CODECS= ['400', '403', '404', '408', '500', '502', '503', '504']
#重试次数
RETRY_TIMES = 10

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded;utf-8',
    'Host': '125.35.6.84:81',
    'Origin': 'http://125.35.6.84:81',
    'Referer': 'http://125.35.6.84:81/xk/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

#--------------------------------------------------------------------------------------
#自动限速扩展，该扩展能根据Scrapy服务器及你爬取的网站的负载自动限制爬取速度
#自动调整scrapy来优化下载速度，使得用户不用调节下载延迟及并发请求数来找到优化的值,
# 用户只需要指定允许的最大并发请求数，剩下的交给扩展来处理
#---------------------------------------------------------------------------------------
AUTOTHROTTLE_ENABLED = True
# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'cosmetics_produce_license.middlewares.CosmeticsProduceLicenseSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'cosmetics_produce_license.middlewares.CosmeticsProduceLicenseDownloaderMiddleware': 543,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 400,
    'cosmetics_produce_license.middlewares.ProxyMiddleware': 100,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'cosmetics_produce_license.pipelines.CosmeticsProduceLicensePipeline': 300,
}

# -------------------------------------------------------
# Mongodb数据存储
# -------------------------------------------------------
MONGO_HOST = '127.0.0.1'
MONGO_PORT = 25000
#用户账号
MONGODB_USER ='raw'
#用户密码
MONGODB_PASSWORD = 'raw_bigdata963qaz'
#数据库名
MONGO_DB = 'raw'
MONGO_COLL = 'drugs_cosmetics_produce_license'

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

from .zhimaip import getdailione
ip, ext_time = getdailione(3) # 调用芝麻IP 3-6个小时