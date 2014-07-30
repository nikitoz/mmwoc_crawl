from scrapy.contrib.spiders import CrawlSpider, Rule;
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor;
from scrapy.selector import HtmlXPathSelector;
from scrapy.spider import BaseSpider;
from parsy.items import CntItem;
from parsy.settings import *
from scrapy.http import *
from sets import Set
import html2text
import nltk
import pymorphy2

class Spider(CrawlSpider):
    name = 'doombringer'
    allowed_domains = []
    start_urls = []
    domain = None
    path   = None
    rules = (
        Rule(SgmlLinkExtractor(allow=('.', )), callback='parse_item'
	, follow=False),
    )

    def __init__(self, domain=None, path=None, *args, **kwargs):
	super(Spider, self).__init__(*args, **kwargs)
	self.allowed_domains = [domain]
        self.start_urls = ['http://' + domain]
	self.domain = domain
	self.path   = path

    def file_name(self):
	return path + domain.replace('.', '_') + '.json'

    def parse_item(self, response) :
	response2 = HtmlResponse(url=response.url, body=response.body)
	page_text = html2text.html2text(response2.body.decode(response2.encoding))
	item = TextItem()
	item['url']  = response.url
	item['text'] = page_text
        return item
