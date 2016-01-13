# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from datetime import datetime
import os

class SmmbmImagesPipeline(ImagesPipeline):
    SUB_DIRECTORY = ''

    def file_path(self, request, response=None, info=None):
        path = super(SmmbmImagesPipeline, self).file_path(request, response, info)
        directory = os.path.join('full', datetime.now().strftime('%Y/%m/%d'), self.SUB_DIRECTORY)
        return path.replace('full', directory, 1)


class CourseImagesPipeline(SmmbmImagesPipeline):
    DEFAULT_IMAGES_URLS_FIELD = 'course_image_urls'
    DEFAULT_IMAGES_RESULT_FIELD = 'course_images'
    SUB_DIRECTORY = 'course'


class CourseFullImagesPipeline(SmmbmImagesPipeline):
    DEFAULT_IMAGES_URLS_FIELD = 'course_full_image_urls'
    DEFAULT_IMAGES_RESULT_FIELD = 'course_full_images'
    SUB_DIRECTORY = 'course_full'


class MiiImagesPipeline(SmmbmImagesPipeline):
    DEFAULT_IMAGES_URLS_FIELD = 'mii_image_urls'
    DEFAULT_IMAGES_RESULT_FIELD = 'mii_images'
    SUB_DIRECTORY = 'mii'
