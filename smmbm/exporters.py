# coding: utf-8
from scrapy.contrib.exporter import BaseItemExporter
import yaml


class YamlItemExporter(BaseItemExporter):
    def __init__(self, file, **kwargs):
        self._configure(kwargs, dont_fail=True)
        self.file = file

    def export_item(self, item):
        itemdict = dict(self._get_serialized_fields(item))
        self.file.write(yaml.dump(itemdict, encoding='utf8', allow_unicode=True))


