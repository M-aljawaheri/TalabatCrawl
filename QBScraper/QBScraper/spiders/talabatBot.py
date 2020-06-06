# -*- coding: utf-8 -*-
import image
import scrapy
from scrapy.shell import inspect_response  # for debugging
from scrapy.http import Request
import sys
sys.path.append('/../../main.py/config')
import main

class TalabatbotSpider(scrapy.Spider):
    name = 'talabatBot'
    mainDomain: str = 'https://www.talabat.com'
    # allowed_domains = ['https://www.talabat.com/qatar/restaurants']
    start_urls = ["https://www.talabat.com/qatar/restaurants"]
    default_location = "al-mansoura"
    custom_settings = {
        'FEED_URI': 'talabat.csv'
    }

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
        data = self.get_JSON_File(response)


        # Test pipeline
        # ------------
        # bypass location by finding where the restaurant delievers and manually entering that
        return scrapy.Request("https://www.talabat.com/qatar/restaurant/44540/al-nasiriya?aid=1732",
                              callback=self.parse_menu_page)
        # ------------

        # Normal pipeline
        #return scrapy.Request(url=self.JSON_Request_URL, dont_filter=True,
        #               callback=self.get_JSON_File)

    # This method gets any json file in a page
    def get_JSON_File(self, response):
        Talabat = TalabatWDSpider(response.url)
        items_list = Talabat.parse()
        return items_list

    # Step 3: Main parse, parse information from the restaurant
    # Parse Menu items / prices / working hours / etc
    def parse_menu_page(self, response):
        x = 5
        # Get the first JSON_File
        pass


# temp garbage
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