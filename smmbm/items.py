# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class CourseItem(Item):
    title = Field()
    skin = Field()
    tag = Field()
    liked_count = Field()
    played_count = Field()
    shared_count = Field()
    tried_count = Field()
    clear_count = Field()
    clear_rate = Field()
    difficulty = Field()

    # CreaterItem
    creater = Field()

    # Image urls
    course_image_urls = Field()
    course_full_image_urls = Field()
    mii_image_urls = Field()


class CreaterItem(Item):
    name = Field()
    country = Field()
    medals = Field()
