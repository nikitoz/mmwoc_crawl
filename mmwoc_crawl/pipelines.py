# coding=utf-8
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import nltk
import re
import pymorphy2
from mmwoc_crawl.items import WocItem
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import codecs
import operator

class MmwocCrawlPipeline(object):
	def process_item(self, item, spider):
		return item

class JsonWithEncodingPipeline(object):
	json_dump = ''

	def open_spider(self, spider):
		self.file = codecs.open(spider.file_name() + '.json', 'w', encoding='utf-8')

	def process_item(self, item, spider):
		line = json.dumps(dict(item), ensure_ascii=False) + "\n"
		self.json_dump = self.json_dump + line
		return item

	def close_spider(self, spider):
		self.file.write(self.json_dump)
		self.file.close()


class ProcessPipeline(object):
	accumulated_words = {}
	forbidden_grammeme = {'NPRO', 'CONJ', 'PRCL', 'INTJ', 'PREP', 'PNCT', 'NUMB', 'UNKN'}
	forbidden_words = {')', '(', '-', ',', '.', '—'}
	words_on_graph = 32

	def process_item(self, item, spider):
		tokens = nltk.word_tokenize(item['text'])
		morph = pymorphy2.MorphAnalyzer()
		cnt = {}
		for tok in tokens:
			tok1 = tok.replace('.', '')
			parsed = morph.parse(tok1)[0]
			
			if (parsed.tag.POS in self.forbidden_grammeme):
				continue
			word = parsed.normal_form
			if (word in self.forbidden_words):
				continue

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
		self.file = codecs.open(spider.file_name() + '_acc.json', 'w', encoding='utf-8')

	def close_spider(self, spider):
		self.file.write(json.dumps(self.accumulated_words, ensure_ascii=False))
		self.file.close()

		reg = re.compile(u'^[а-яА-Я]+$', re.UNICODE)
		
		sorted_file = codecs.open(spider.file_name() + '_graph.json', 'w', encoding='utf-8')		
		sorted_data = sorted(self.accumulated_words.iteritems(), key=operator.itemgetter(1), reverse=True)
		a, b = [ e[0] for e in sorted_data if (reg.match(e[0]) != None) ], [e[1] for e in sorted_data]
			
		sorted_file.write(json.dumps({'words' : a[0:self.words_on_graph], 'occurrences' : b[0:self.words_on_graph]} , ensure_ascii=False))
		sorted_file.close()
