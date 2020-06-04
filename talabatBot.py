# -*- coding: utf-8 -*-
import scrapy
'''from bs4 import BeautifulSoup
import requests'''
# Beautiful soup is used to extract all the restaurant URLs
## that the spider will crawl through eventually
class TalabatbotSpider(scrapy.Spider):
    name = 'talabatBot'
    mainDomain: str = 'https://www.talabat.com/qatar/restaurants'

    '''
    # Spoof our identity
    headers = requests.utils.default_headers()
    headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})
    # Fetch HTML file from talabat restaurant menu
    req = requests.get(mainDomain, headers)
    # Making the soup object
    soup = BeautifulSoup(req.content, 'html.parser')
    tempList = [link.get('href') for link in soup.final_all('a')]
    '''

    # allowed_domains = ['https://www.talabat.com/qatar/restaurants']
    start_urls = ['https://www.talabat.com/qatar/restaurants']
    custom_settings = {
        'FEED_URI': 'talabat.csv'
    }

    # Parse is called whenever the spider successfully crawls a URL
    # Response object is automatically filled with page info and passed to parse

    # Step 1: Main parse callback, crawling starts here
    ## Gather: None
    ## Fetch : All restaurant links
    def Parse(self, response):
        # Here we extract the information we want from the response
        for restaurant in response.xpath("//a[contains(@href, '/restaurants)]/@href").extract():
            yield scrapy.Request(response.urljoin())


        # Zip all parsed info, put into one dictionary (our main object)

        # yield item
        pass


    # Step 2: Parsing individual restaurant pages
    ## Gather: basic info (e.g Restaurant Name)
    ## Fetch : Link to Menu page
    def ParseRestaurantPage(self, response):
        pass


    # Step 3: Main parse, parse information from the restaurant
    ## Parse Menu items / prices / working hours / etc
    def ParseMenuPage(self, response):
        pass