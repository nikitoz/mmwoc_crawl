scrapy crawl doombringer -a site="lenta.ru" -a domain="lenta.ru" -a path="../data/"             &&
scrapy crawl doombringer -a site="vesti.ru" -a domain="vesti.ru" -a path="../data/"             &&
scrapy crawl doombringer -a site="ria.ru"   -a domain="ria.ru"   -a path="../data/"             &&
scrapy crawl doombringer -a site="newsru.com" -a domain="newsru.com" -a path="../data/"         &&
scrapy crawl doombringer -a site="kp.ru" -a domain="kp.ru" -a path="../data/"                   &&
scrapy crawl doombringer -a site="lifenews.ru" -a domain="lifenews.ru" -a path="../data/"       &&
scrapy crawl doombringer -a site="russian.rt.com" -a domain="russian.rt.com" -a path="../data/" &&
echo "Done"

