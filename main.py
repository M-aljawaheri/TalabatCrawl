######## QB WebCrawler ########
# @author: Mohammed Al-jawaheri
# @date  : 6/4/2020
###############################
from typing import *  # using type annotations for runtime checks
import scrapy
# Restaurant object holds restaurant information + a list of foodItem objects
# Fooditem objects wrap a given food item info in a single structure


# Defining the main objects to be dumped in JSON
class FoodItem:
    def __init__(self, name, desc, price):
        self.name: str = name
        self.desc: str = desc
        self.price: float = price
        self.photo = ''


class Restaurant:
    def __init__(self, name, desc):
        self.name: str = name
        self.desc: str = desc
        self.menuItems = []
        self.photo = ''


def main():
    return 1
