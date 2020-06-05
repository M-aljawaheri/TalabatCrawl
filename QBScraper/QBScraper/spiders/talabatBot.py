# -*- coding: utf-8 -*-
import image
import scrapy
import re
from scrapy.shell import inspect_response  # for debugging

'''from bs4 import BeautifulSoup
import requests'''
# Beautiful soup is used to extract all the restaurant URLs
## that the spider will crawl through eventually
class TalabatbotSpider(scrapy.Spider):
    name = 'talabatBot'
    mainDomain: str = 'https://www.talabat.com'

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
    start_urls = ["https://www.talabat.com/qatar/restaurants"]
    default_location = "al-mansoura"
    custom_settings = {
        'FEED_URI': 'talabat.csv'
    }

    # Parse is called whenever the spider successfully crawls a URL
    # Response object is automatically filled with page info and passed to parse

    # Step 1: Main parse callback, crawling starts here
    ## Gather: None
    ## Fetch : All restaurant links
    def parse(self, response):
        x = 5
        #inspect_response(response, self) TODO: send requests for more links once you're done
        #filter(lambda x: x != '/qatar/restaurants',)
        for restaurant in response.xpath("//a[contains(@href, '/qatar')]/@href").extract()[16:-39]:
            yield scrapy.Request(response.urljoin(self.mainDomain + restaurant), callback=self.parse_restaurant_page)



    # Step 2: Parsing individual restaurant pages
    ## Gather: basic info (e.g Restaurant Name)
    ## Fetch : Link to Menu page
    def parse_restaurant_page(self, response):
        #inspect_response(response, self)

        # Get the json file containing all restaurant information

        # bypass location by adding default mainlocation to URL
        # and continue to menu items page
        # response.urljoin
        x = 5
        pass


    # Step 3: Main parse, parse information from the restaurant
    ## Parse Menu items / prices / working hours / etc
    def parse_menu_page(self, response):
        pass
