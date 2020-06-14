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
        'FEED_URI': 'talabatJSONdebugBIG.json'
    }
    item_num = 0
    possibleLocations = ['ain-khaled?aid=1740', 'onaiza?aid=1700']
    restaurant_advanced_info = []
    dataList = []

    # Data processing methods
    def fix_data_file(self, data):
        data['type'] = data['@type']
        data['context'] = data['@context']
        del data['@type']
        del data['@context']
        del data['@id']
        del data['image']   # On the assumption that logo == image TODO: recheck

    def fix_JSON_format(self, obj):
        new_json = {}   # put menu section after it was modified in here
        new_json['menuSections'] = []
        new_json['menu_id'] = obj['result']['menu']['id']

        menuSection = obj['result']['menu']['menuSection'] # a list of menu sections
        for section in menuSection:
            new_json['menuSections'].append({'sectionName': section['nm'], 'items': self.fix_item_list(section['itm']) })

        return new_json

    def fix_item_list(self, item_list):
        new_item_list = []
        for item in item_list:
            new_item = {'name'   : item['nm'],
                        'itemID' : item['id'],
                        'rating' : item['rt'],
                        'price'  : item['pr'],
                        'image'  : item['img'],
                        'description' : item['dsc']}
            new_item_list.append(new_item)

        return new_item_list

    # Parse is called whenever the spider successfully crawls a URL
    # Response object is automatically filled with page info and passed to parse
    def parse(self, response):
        """
        Step 1: Main parse callback, crawling starts here "talabat/qatar/allRestaurants"
        Gather: None
        Fetch : All restaurant links
        """

        #return scrapy.Request("https://www.talabat.com/qatar/Oishi-Sushi-Authentic-Japanese-Restaurant", callback=self.parse_restaurant_page)
        # ------ NORMAL PIPELINE ---------
        # TODO: send requests for more links once you're done
        # scroll down to the end of the page to get all links
        restaurant_list = webdriver.runScrollDriver(self.start_urls[0])
        #for restaurant in response.xpath("//a[contains(@href, '/qatar')]/@href").extract()[16:-39]:
        for restaurant in restaurant_list:
            yield scrapy.Request(f"{self.mainDomain}/qatar/{restaurant}", callback=self.parse_restaurant_page)
        # ----- END NORMAL PIPELINE ------


        ## ------- TEST PIPELINE ----------
        #
        #restaurant = 'arabesque'
        #return scrapy.Request(f"{self.mainDomain}/qatar/{restaurant}", callback=self.parse_restaurant_page)
        ## --------  END TEST  ------------

    def parse_restaurant_page(self, response):
        """
        Step 2: Parsing individual restaurant pages "talabat/qatar/specificRestaurant"
        Gather: basic info (e.g Restaurant Name)
        Fetch : Link to Menu page
        """

        # 1) Get the json file containing all restaurant information
        try:
            self.data = self.get_JSON_File(response)[0]
            if (self.data['@type'] != 'Restaurant' and self.data['@type'] != 'restaurant'):
                return {response.url : 'Not restaurant'}
            self.fix_data_file(self.data)
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
            self.item_num += 1
            while (len(self.restaurant_advanced_info) < len(self.dataList)):
                self.restaurant_advanced_info.append(None)
            return {response.url : self.data}

        # Normal pipeline
        # ----------------
        # Get URL to menu page
        menu_url = f"https://www.talabat.com/qatar/restaurant/{restaurant_ID}/{valid_location}?aid={aid}"
        return scrapy.Request(menu_url, callback=self.parse_menu_page)
        # ----------------

    def get_JSON_File(self, response):
        """ Method to get JSON file from a url """
        items_list = webdriver.runWebDriverJSON(response.url)
        return items_list

    # Step 3: Main parse, parse information from the restaurant
    # Parse Menu items / prices / working hours / etc
    def parse_menu_page(self, response):
        if response.url == 'https://www.talabat.com/qatar':
            self.item_num += 1
            return {f"could not parse {self.dataList[-1]['url']}": None}
        self.restaurant_advanced_info.append(webdriver.runWebDriverMenuPage(response.url))
        self.restaurant_advanced_info[-1] = self.fix_JSON_format(self.restaurant_advanced_info[-1])
        self.item_num += 1
        if (self.restaurant_advanced_info[self.item_num-1] and self.dataList[self.item_num-1]):
            return { str(self.item_num-1): {**self.dataList[self.item_num-1], **self.restaurant_advanced_info[self.item_num-1]} }





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
