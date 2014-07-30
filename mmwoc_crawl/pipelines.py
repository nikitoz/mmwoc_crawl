# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class MmwocCrawlPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonWithEncodingPipeline(object):
    json_dump = ''

    def spider_opened(self, spider):
	self.file = codecs.open(spider.file_name(), 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
	json_dump = json_dump + line
        return item

    def spider_closed(self, spider):
        self.file.write(json_dump)
        self.file.close()

class ProcessPipeline(object):
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
        return ret_item
	
