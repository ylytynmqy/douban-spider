# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class DoubanItem(Item):
    collection = 'film'
    id = Field()
    title = Field()
    year = Field()
    rate = Field()
    rating_num = Field()
    tags = Field()
    director= Field()
    actor=Field()