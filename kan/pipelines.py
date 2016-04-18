# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import os
from collections import OrderedDict

import scrapy
from scrapy.pipelines.files import FilesPipeline

#generate the html file
class KanPipeline(object):
    def __init__(self):
        self.file = codecs.open('list.html', 'wb+', encoding='utf-8')
        self.file.write("<html>")
        self.file.write("<body>")
        self.file.write("<table>")

    def process_item(self, item, spider):
        # line = json.dumps(dict(item), ensure_ascii=False, sort_keys=True) + "\n"
        self.file.write("<tr>")
        self.file.write("<td> %s</td>" % ''.join(item['book_title']))
        self.file.write("<td><a href=%s> %s</td>" % (''.join(item['file_urls']), ''.join(item['file_urls'])))
        self.file.write("</tr>")
        return item

    def spider_closed(self, spider):
        self.file.write("</table>")
        self.file.write("</body>")
        self.file.write("</html>")
        self.file.close()

#download the file
class MyFilePipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        if item['file_urls'] is not None:
            yield scrapy.Request(item['file_urls'])

    def item_completed(self, results, item, info):
        file_paths = [x['path'] for ok, x in results if ok]
        if not file_paths:
            return None
        new_name = ''.join(item['book_title']) + '.mobi'
        os.rename('d:/mobi/' + file_paths[0], 'd:/mobi/full/' + new_name)
        return item
