# -*- coding: utf-8 -*-
import image
import scrapy
import json
import re
import requests
from bs4 import BeautifulSoup
from scrapy.shell import inspect_response  # for debugging
from scrapy.http import Request
#from selenium import webdriver

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

    JSON_Request_URL: str = "https://www.talabat.com/apps/dist/talabat/components/info/infoController.js?v=2020-06-01T09:19:25.0278186"
    # Parse is called whenever the spider successfully crawls a URL
    # Response object is automatically filled with page info and passed to parse

    # Step 1: Main parse callback, crawling starts here "talabat/qatar/allRestaurants"
    # Gather: None
    # Fetch : All restaurant links
    def parse(self, response):
        # TODO: send requests for more links once you're done
        for restaurant in response.xpath("//a[contains(@href, '/qatar')]/@href").extract()[16:-39]:
            yield scrapy.Request(response.urljoin(self.mainDomain + restaurant), callback=self.parse_restaurant_page)



    # Step 2: Parsing individual restaurant pages "talabat/qatar/specificRestaurant"
    # Gather: basic info (e.g Restaurant Name)
    # Fetch : Link to Menu page
    def parse_restaurant_page(self, response):
        #inspect_response(response, self)
        # 1) Get the json file containing all restaurant information
        data = self.get_ld_json(response.url)
        return scrapy.Request(url=self.JSON_Request_URL, dont_filter=True,
                       callback=self.get_JSON_File)


        # bypass location by adding default mainlocation to URL
        # and continue to menu items page with response.urljoin

    def get_JSON_File(self, response):
        data = self.get_ld_json(response.url)
        x=5


    def get_ld_json(self, url: str) -> dict:
        parser = "html.parser"
        req = requests.get(url)
        soup = BeautifulSoup(req.text, parser)
        return json.loads("".join(soup.find("script", {"type":"application/ld+json"}).contents))


    # Step 3: Main parse, parse information from the restaurant
    # Parse Menu items / prices / working hours / etc
    def parse_menu_page(self, response):
        pass
