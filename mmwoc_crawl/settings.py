# Scrapy settings for mmwoc_crawl project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'mmwoc_crawl'

SPIDER_MODULES = ['mmwoc_crawl.spiders']
NEWSPIDER_MODULE = 'mmwoc_crawl.spiders'

DEPTH_LIMIT = 1
ITEM_PIPELINES = ['mmwoc_crawl.pipelines.ProcessPipeline']

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7'

CONCURRENT_REQUESTS = 100
LOG_LEVEL = 'INFO'
DOWNLOAD_TIMEOUT = 15
AJAXCRAWL_ENABLED = True
MONGO_DESTINATION = 'mongodb://localhost:27017/'