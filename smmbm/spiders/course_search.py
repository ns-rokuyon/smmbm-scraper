# coding: utf-8
import re
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector

from smmbm.items import CourseItem, CreaterItem

class CourseSearchSpider(CrawlSpider):
    ''' Super Mario Maker BookMark crawler '''

    name = 'course_search'
    allowed_domains = ['supermariomakerbookmark.nintendo.net']

    page_max = 1    # Max 10
    start_urls = [ 'https://supermariomakerbookmark.nintendo.net/search/result?page=%d&q%%5Bsorting_item%%5D=like_rate_desc&utf8=%%E2%%9C%%93' \
                % (page + 1) for page in xrange(page_max) ]

    typography_regexp = re.compile('typography typography-([0-9]|second)')

    def parse(self, response):
        ''' Parse course search results '''
        for course_card in response.xpath('//div[@class="course-card"]'):
            course = CourseItem()
            creater = CreaterItem()

            # Creater info
            creater['name'] = course_card.xpath('.//div[@class="name"]/text()').extract()[0]
            course['creater'] = creater

            # Image urls
            course['course_image_urls'] = course_card.xpath('.//img[@class="course-image"]/@src').extract()
            course['course_full_image_urls'] = course_card.xpath('.//img[@class="course-image-full"]/@src').extract()
            course['mii_image_urls'] = course_card.xpath('.//a[@id="mii"]').xpath('.//img/@src').extract()

            # Clear rate
            course['clear_rate'] = self.__clear_rate(course_card.xpath('.//div[@class="clear-rate"]/div/@class').extract())

            # Counts
            course['liked_count'] = self.__typography2int(
                    course_card.xpath('.//div[contains(@class,"liked-count")]/div[contains(@class,"typography")]/@class').extract()[0])
            course['played_count'] = self.__typography2int(
                    course_card.xpath('.//div[contains(@class,"played-count")]/div[contains(@class,"typography")]/@class').extract()[0])
            course['shared_count'] = self.__typography2int(
                    course_card.xpath('.//div[contains(@class,"shared-count")]/div[contains(@class,"typography")]/@class').extract()[0])

            # Course title
            course['title'] = course_card.xpath('.//div[@class="course-title"]/text()').extract()[0]

            # Course tag
            course['tag'] = course_card.xpath('.//div[contains(@class,"course-tag")]/text()').extract()[0]

            yield course

    def __clear_rate(self, css_classes):
        s = ''.join([ x for x in map(self.__parse_typography, css_classes) if x is not None])
        return float(s)

    def __parse_typography(self, c):
        m = self.typography_regexp.match(c)
        if m is None:
            return None
        num = m.group(1)
        if num == 'second':
            return '.'
        return num

    def __typography2int(self, css_class):
        s = self.__parse_typography(css_class)
        if s is None:
            return None
        return int(s)
