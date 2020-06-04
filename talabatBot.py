# -*- coding: utf-8 -*-
import scrapy


class TalabatbotSpider(scrapy.Spider):
    name = 'talabatBot'
    allowed_domains = ['https://www.talabat.com/qatar/restaurants']
    start_urls = ['http://https://www.talabat.com/qatar/restaurants/']

    def parse(self, response):
        pass
