import spiders.talabatBot as sp
from scrapy.crawler import CrawlerProcess

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    # 'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
    'FEED_FORMAT': 'json',
    'FEED_URI': 'data.json'
})

process.crawl(sp.TalabatbotSpider)
process.start()  # the script will block here until the crawling is finished
