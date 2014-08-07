from scrapy.contrib.spiders import CrawlSpider, Rule;
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor;
from scrapy.selector import HtmlXPathSelector;
from scrapy.spider import BaseSpider;
from mmwoc_crawl.items import TextItem;
from mmwoc_crawl.settings import *
from scrapy.http import *
from sets import Set
import html2text
import pymorphy2
import datetime
from scrapy.contrib.linkextractors import LinkExtractor

class Spider(CrawlSpider):
	name = 'doombringer'
	allowed_domains = []
	start_urls = []
	domain = None
	path   = None
	site = None
	rules = (
		Rule(LinkExtractor(unique=True), callback='parse_start_url', follow=True),
		Rule(LinkExtractor(unique=True), callback='parse_item', follow=True),
	)

	def __init__(self, site=None, domain=None, path=None, *args, **kwargs):
		super(Spider, self).__init__(*args, **kwargs)
		self.allowed_domains = [domain]
		self.start_urls = ['http://' + site]
		self.domain = domain
		self.path   = path
		self.site = site
        
	def file_name(self):
		return self.path + self.site.replace('.', '').replace('/', '') + '_' + datetime.date.today().strftime('%d_%m_%y')

	def parse_start_url(self, response):
		return self.parse_item(response)

	def parse_item(self, response) :
		response2 = HtmlResponse(url=response.url, body=response.body)
		try:
			page_text = html2text.html2text(response2.body.decode(response2.encoding))
		except:
			page_text = ''
		item = TextItem()
		item['url']  = response.url
		item['text'] = page_text
		return item