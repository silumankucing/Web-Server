import scrapy


class TlkmSpider(scrapy.Spider):
    name = 'tlkm'
    allowed_domains = ['cnbcindonesia.com']
    start_urls = ['http://cnbcindonesia.com/']

    def parse(self, response):
        pass
