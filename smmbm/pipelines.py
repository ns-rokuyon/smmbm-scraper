# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from datetime import datetime
import os
import pymongo

class SmmbmImagesPipeline(ImagesPipeline):
    SUB_DIRECTORY = ''

    @classmethod
    def from_settings(cls, settings):
        pipeline = super(SmmbmImagesPipeline, cls).from_settings(settings)
        pipeline.mongo_server = settings.get('MONGODB_SERVER')
        pipeline.mongo_port = settings.get('MONGODB_PORT')
        pipeline.mongo_dbname = settings.get('MONGODB_DB')
        pipeline.mongo_collection = settings.get('MONGODB_COLLECTION')
        return pipeline

    def open_spider(self, spider):
        super(SmmbmImagesPipeline, self).open_spider(spider)
        self.conn = pymongo.MongoClient(self.mongo_server, self.mongo_port)
        self.course_collection = self.conn[self.mongo_dbname][self.mongo_collection]

    def close_spider(self, spider):
        self.conn.close()

    def item_completed(self, results, item, info):
        _item = super(SmmbmImagesPipeline, self).item_completed(results, item, info)
        db_item = dict(_item)
        db_item['_id'] = _item['course_id']
        self.course_collection.save(db_item)
        return _item

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
