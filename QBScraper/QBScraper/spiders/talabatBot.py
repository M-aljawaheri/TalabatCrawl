# -*- coding: utf-8 -*-
import image
import scrapy
import re
from scrapy.shell import inspect_response  # for debugging
from scrapy.http import Request
import os, sys; sys.path.append(os.path.dirname(os.path.realpath('webdriver.py')))
from . import webdriver


class restaurantInfo:
    def __init__(self, basic_data, advanced_data):
        self.basic_d = basic_data
        self.advanced_d = advanced_data


class TalabatbotSpider(scrapy.Spider):
    name = 'talabatBot'
    mainDomain: str = 'https://www.talabat.com'
    # allowed_domains = ['https://www.talabat.com/qatar/restaurants']
    start_urls = ["https://www.talabat.com/qatar/restaurants"]
    default_location = "al-mansoura"
    custom_settings = {
        'FEED_URI': 'talabat7.csv'
    }
    item_num = 0
    restaurant_advanced_info = []
    dataList = []
    # Parse is called whenever the spider successfully crawls a URL
    # Response object is automatically filled with page info and passed to parse

    def parse(self, response):
        """
        Step 1: Main parse callback, crawling starts here "talabat/qatar/allRestaurants"
        Gather: None
        Fetch : All restaurant links
        """

        # TODO: send requests for more links once you're done
        for restaurant in response.xpath("//a[contains(@href, '/qatar')]/@href").extract()[16:-39]:
            yield scrapy.Request(response.urljoin(self.mainDomain + restaurant), callback=self.parse_restaurant_page)

    def parse_restaurant_page(self, response):
        """
        Step 2: Parsing individual restaurant pages "talabat/qatar/specificRestaurant"
        Gather: basic info (e.g Restaurant Name)
        Fetch : Link to Menu page
        """

        # 1) Get the json file containing all restaurant information
        try:
            self.data = self.get_JSON_File(response)[0]
            self.dataList.append(self.data)
            # restaurant_ID = re.findall("\d\d\d\d\d", response.css("script").extract()[22])[29]
            restaurant_ID = re.findall("bid:\d\d\d\d\d", response.css("script").extract()[22])[0][4:]
            #valid_location = re.search("Al \w+", self.data['description']).group().replace(" ", "-")
            valid_locations = re.findall("Al \w+", self.data['description'])
            if (len(valid_locations) == 0):
                valid_locations = re.search("Umm \w+", self.data['description']).group()
            # mainModel JSON
            #------
            # response.xpath('/html/body/script[13]').extract()
            text = response.xpath("//script[@type='text/javascript']").extract()[8]
            ## id:1754,cid:45,cn:"Doha",an:"Abu Hamour "
            result = re.search('id:\d\d\d\d,cid:\d\d,cn:"\w+",an:"\D+"', text).group()
            result = result.split('"')
            valid_location = result[-2].replace(" ", "-")
            aid = result[0][3:7]
            #------

            #if len(valid_locations) > 2:
            #    valid_location = valid_locations[2].replace(" ", "-")
            #else:
            valid_location = valid_locations[0].rstrip().replace(" ", "-")
        except:
            yield {'item1' : None}

        # Normal pipeline
        # ----------------
        # Get URL to menu page
        menu_url = f"https://www.talabat.com/qatar/restaurant/{restaurant_ID}/{valid_location}?aid={aid}"
        yield scrapy.Request(menu_url, callback=self.parse_menu_page)
        # ----------------

    def get_JSON_File(self, response):
        """ Method to get JSON file from a url """
        items_list = webdriver.runWebDriverJSON(response.url)
        return items_list

    # Step 3: Main parse, parse information from the restaurant
    # Parse Menu items / prices / working hours / etc
    def parse_menu_page(self, response):
        self.restaurant_advanced_info.append(webdriver.runWebDriverMenuPage(response.url))
        self.restaurant_advanced_info = fix_JSON_format(self.restaurant_advanced_info)
        self.item_num += 1
        if (self.restaurant_advanced_info[self.item_num-1] and self.dataList[self.item_num-1]):
            yield { str(self.item_num-1): {**self.dataList[self.item_num-1], **self.restaurant_advanced_info[self.item_num-1]} }

def fix_JSON_format(obj):
    return obj

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



#-------------menu_url = f"https://www.talabat.com/qatar/restaurant/{restaurant_ID}/{valid_location}?aid=1732"
menu_url = f"https://www.talabat.com/qatar/restaurant/{restaurant_ID}/{valid_location}"

'''
