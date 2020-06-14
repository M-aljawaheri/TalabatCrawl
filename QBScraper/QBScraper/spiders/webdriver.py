# ####### QB WebCrawler ########
# @author: Mohammed Al-jawaheri
# @date  : 6/4/2020
###############################
# !/bin/python
# -*- coding: utf-8 -*-

from time import sleep
from random import randint
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import json
import re


class TalabatWDSpider():
    """
    DESCRIPTION
    -------
        Webdriver class. can be used to render dynamic JS in page and extract
        Information using BeauitfulSoup

    METHODS
    -------
    - parse()

        All other methods are internal. Instantiate by passing a URL get a list of items
        using METHOD:parse()
    """

    def __init__(self, url):
        self.url_to_crawl = url
        self.all_items = []

    # Open headless chromedriver
    def start_driver(self):
        print('----\nstarting driver...\n----')
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        # specify the desired user agent
        chrome_options.add_argument(f'user-agent={user_agent}')
        self.driver = webdriver.Chrome("C:\\Users\\M_alj\\Downloads\\chromedriver_win32 (2)\\chromedriver.exe", options=chrome_options)
        sleep(4)

    # Close chromedriver
    def close_driver(self):
        print('----\nclosing driver...\n----')
        self.driver.quit()
        print('closed!')

    # Tell the browser to get a page
    def get_page(self, url):
        print(f'----\ngetting page...\npage is...{url}\n----')
        self.driver.get(url)
        for cookie in self.driver.get_cookies():
            self.driver.add_cookie(cookie)
        sleep(randint(2, 3))


class mainPageSpider(TalabatWDSpider):
    # Adds to all_items a JSON object with restaurant data
    def grab_restaurant_info(self):
        """
            @param   : None
            @rtype   : JSON obj (dict)
            @returns : JSON obj {Name, image, ratings, description, etc}
        """

        print('----\ngrabbing list of items...\n----')
        try:
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'lxml')
            restaurant_info_JSON = [json.loads("".join(info.contents)) for info in soup.find_all("script", {"type": "application/ld+json"})]
            if len(restaurant_info_JSON) == 1:
                restaurant_info_JSON = restaurant_info_JSON[0]
            # TODO: fix formatting of JSON
            self.all_items.append(restaurant_info_JSON)
        except:
            pass

    def parse(self):
        """
            Main Method
        @params : None
        @rtype  : JSON obj (dict)
        @returns: Restaurant info
        """

        self.start_driver()
        self.get_page(self.url_to_crawl)
        self.grab_restaurant_info()
        self.close_driver()

        if self.all_items:
            return self.all_items[0]
        # If getting all items fails
        return False


class MenuPageSpider(TalabatWDSpider):

    def grab_menu_info(self):
        """ How we get menu items <--- """  # 44540
        try:
            headers = requests.utils.default_headers()
            headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})
            # Fetch HTML file from talabat restaurant menu
            restaurant_num = re.search("\d+", self.driver.current_url).group()
            req = requests.get(f"https://www.talabat.com/menuapi/v2/branches/{restaurant_num}/menu", headers)
            soup = BeautifulSoup(req.content, 'lxml')
            self.all_items.append(json.loads(soup.string))
        except:
            pass

    def parse(self):
        """
            Main Method
        @params : None
        @rtype  : JSON obj (dict)
        @returns: Restaurant info
        """

        self.start_driver()
        self.get_page(self.url_to_crawl)
        self.grab_menu_info()
        self.close_driver()

        if self.all_items:
            return self.all_items[0]
        # If getting all items fails
        return False

from selenium.webdriver.common.keys import Keys

class scrollerDriver(TalabatWDSpider):
    def scrollDown(self):
        pause = 0.5
        offset = 1000
        lastHeight = self.driver.execute_script(f"return document.body.scrollHeight-{offset}")
        while True:
            offset = offset - 200 if offset > 400 else 400
            self.driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight-{offset});")
            sleep(pause)
            newHeight = self.driver.execute_script("return document.body.scrollHeight")
            if newHeight == lastHeight:
                break
            lastHeight = newHeight

    def getSoup(self):
        # Category labels are forbidden; we want restaurants
        forbiddenLabels = [
            "Thai", "Healthy-food", "Healthy-Food", "Indian", "Cafe",
            "Grocery", "Desserts", "Turkish", "Flowers", "Qatari",
            "Mexican", "Pharmacy", "Italian", "Turkish", "Egyptian",
            "Arabic", "Monoprix", "International", "Electronics", "Pasta",
            "Burgers", "Lebanese", "American", "Breakfast", "pizzas",
            "Asian", "Cosmetics", "Specialty-Store", "Beverages", "Iranian",
            "Japanese", "Feedback", "Careers", "Terms", "FAQ", "Health-and-Beauty-Pharmacy",
            "Privacy", "Contact-Us", "Sitemap", "Dermacol-Cosmetics-&-Skin-Care",
            "Pick-And-Save-Supermarket", "International-Foodstuff-Group-I-F-G"
        ]
        headers = requests.utils.default_headers()
        headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})
        # Fetch HTML file from talabat restaurant menu
        req = requests.get(self.driver.current_url)
        soup = BeautifulSoup(req.content, 'lxml')
        #allRestaurants = [x.text[:x.text.find("\n")].replace(" ", "-") for x in self.driver.find_elements_by_xpath("//a[contains(@href, '/qatar')]") if x.text != '' and ',' not in x.text and x.text[:x.text.find("\n")].replace(" ", "-") not in forbiddenLabels]
        # Unrolled loop comprehension (saves up on redundant operations)
        allRestaurants = []
        for restaurant in self.driver.find_elements_by_xpath("//a[contains(@href, '/qatar')]"):
            if restaurant.text != '' and ',' not in restaurant.text:
                newline_index = restaurant.text.find("\n")
                processed_name = restaurant.text[:newline_index].replace(" ", "-") if newline_index != -1 else restaurant.text.replace(" ", "-")

                if processed_name not in forbiddenLabels:
                    allRestaurants.append(processed_name)



        return allRestaurants

    def parse(self):
        self.start_driver()
        self.get_page(self.url_to_crawl)
        self.scrollDown()
        rest_list = self.getSoup()
        self.close_driver()

        return rest_list

def runWebDriverJSON(url):
    """
        Interface Function, webdriver wrapper that user accesses
    @params : (str) URL
    @rtype  : JSON obj (dict)
    @returns: JSON of restaurant information
    """

    # Run webdriver spider
    Talabat = mainPageSpider(url)
    items_list = Talabat.parse()
    return items_list


def runWebDriverMenuPage(url):
    # Run webdriver spider
    Talabat = MenuPageSpider(url)
    items_list = Talabat.parse()
    return items_list


def runScrollDriver(url):
    Talabat = scrollerDriver(url)
    return Talabat.parse()


if (__name__ == "__main__"):
    testurl = "https://www.talabat.com/qatar/restaurant/44540/al-nasiriya?aid=1732"
    runWebDriver(testurl)


"""
---prototype1---
old_position = 0
new_position = None

while new_position != old_position:
    # Get old scroll position
    old_position = self.driver.execute_script(("return (window.pageYOffset !== undefined) ? window.pageYOffset : (document.documentElement || document.body.parentNode || document.body);"))
    # Sleep and Scroll
    sleep(1)
    self.driver.execute_script(("var scrollingElement = (document.scrollingElement || document.body);scrollingElement.scrollTop = scrollingElement.scrollHeight;"))
    # Get new position
    new_position = self.driver.execute_script(("return (window.pageYOffset !== undefined) ? window.pageYOffset : (document.documentElement || document.body.parentNode || document.body);"))

"""
