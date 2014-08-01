# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import nltk
import pymorphy2
from mmwoc_crawl.items import WocItem
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import codecs

class MmwocCrawlPipeline(object):
	def process_item(self, item, spider):
		return item

class JsonWithEncodingPipeline(object):
	json_dump = ''

	def open_spider(self, spider):
		self.file = codecs.open(spider.file_name(), 'w', encoding='utf-8')

	def process_item(self, item, spider):
		line = json.dumps(dict(item), ensure_ascii=False) + "\n"
		self.json_dump = self.json_dump + line
		return item

	def close_spider(self, spider):
		self.file.write(self.json_dump)
		self.file.close()


class ProcessPipeline(object):
	accumulated_words = {}

	def process_item(self, item, spider):
		tokens = nltk.word_tokenize(item['text'])
		morph = pymorphy2.MorphAnalyzer()
		cnt = {}
		for tok in tokens:
			tok1 = tok.replace('.', '')
			word = morph.parse(tok1)[0].normal_form
			if (not word in cnt):
				cnt[word] = 0
			cnt[word] = cnt[word] + 1
		ret_item = WocItem()
		ret_item['url'] = item['url']
		ret_item['stuff'] = cnt

		for key in cnt.keys():
			if (key in self.accumulated_words):
				self.accumulated_words[key] = self.accumulated_words[key] + cnt[key]
			else:
				self.accumulated_words[key] = cnt[key]
		return ret_item

	def open_spider(self, spider):
		self.file = codecs.open(spider.file_name().replace('.json', '_acc.json'), 'w', encoding='utf-8')

	def close_spider(self, spider):
		self.file.write(json.dumps(self.accumulated_words, ensure_ascii=False))
		self.file.close()
