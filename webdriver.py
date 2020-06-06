######## QB WebCrawler ########
# @author: Mohammed Al-jawaheri
# @date  : 6/4/2020
###############################
#!/bin/python
# -*- coding: utf-8 -*-

from time import sleep
from random import randint
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json


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
        print('starting driver...')
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        # specify the desired user agent
        chrome_options.add_argument(f'user-agent={user_agent}')
        self.driver = webdriver.Chrome("C:\\Users\\M_alj\\Downloads\\chromedriver_win32 (2)\\chromedriver.exe", options=chrome_options)
        sleep(4)

    # Close chromedriver
    def close_driver(self):
        print('closing driver...')
        self.driver.quit()
        print('closed!')

    # Tell the browser to get a page
    def get_page(self, url):
        print('getting page...\npage is...' + url)
        self.driver.get(url)
        for cookie in self.driver.get_cookies():
            self.driver.add_cookie(cookie)
        sleep(randint(2, 3))

    # Adds to all_items a JSON object with restaurant data
    def grab_restaurant_info(self):
        """
            @param   : None
            @rtype   : JSON obj (dict)
            @returns : JSON obj {Name, image, ratings, description, etc}
        """

        print('grabbing list of items...')
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        restaurant_info_JSON = [json.loads("".join(info.contents)) for info in soup.find_all("script", {"type":"application/ld+json"})]
        if len(restaurant_info_JSON) == 1:
            restaurant_info_JSON = restaurant_info_JSON[0]
        # TODO: fix formatting of JSON
        self.all_items.append(restaurant_info_JSON)

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
            return self.all_items
        # If getting all items fails
        return False


def runWebDriver(url):
    """
        Interface Function, webdriver wrapper that user accesses
    @params : (str) URL
    @rtype  : JSON obj (dict)
    @returns: JSON of restaurant information
    """

    # Run webdriver spider
    Talabat = TalabatWDSpider(url)
    items_list = Talabat.parse()
    return items_list


runWebDriver("https://www.talabat.com/qatar/fajitas-mexican-grill1")