# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import os
from collections import OrderedDict

import MySQLdb
import re
import scrapy
from scrapy.pipelines.files import FilesPipeline


# generate the html file
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
        self.file.write("<td> %s</td>" % ''.join(item['author']).decode('utf-8', errors='ignore'))
        self.file.write("<td><a href=%s> %s</td>" % (''.join(item['file_urls'][0]), ''.join(item['file_urls'][0])))
        self.file.write("<td> %s</td>" % ''.join(item['description']))
        self.file.write("</tr>")
        return item

    def spider_closed(self, spider):
        self.file.write("</table>")
        self.file.write("</body>")
        self.file.write("</html>")
        self.file.close()


# download the file
class MyFilePipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        if item['file_urls'][0] is not None:
            yield scrapy.Request(item['file_urls'][0])

    def item_completed(self, results, item, info):
        file_paths = [x['path'] for ok, x in results if ok]
        if not file_paths:
            return None
        r = re.compile(r"\r|\n")
        new_name = ''.join(item['book_title'])
        # delete otiose sign
        new_name = re.sub(r, "", new_name)
        os.rename('F:/mobi/' + file_paths[0], 'F:/mobi/full/' + new_name)
        return item


# inset into DateBase
class DateBasePipeline(object):
    def __init__(self):
        self.db = MySQLdb.connect("localhost", "root", "laojiaqi", "mobi", charset='utf8')
        self.cursor = self.db.cursor()
        self.count = 0

    def process_item(self, item, spider):
        sql = "insert into mobi(content,url,author,description) values(%s,%s,%s,%s)"
        if len(''.join(item['file_urls'])) < 5:
            return item
        try:
            self.cursor.execute(sql, (''.join(item['book_title']), ''.join(item['file_urls'][0]), ''.join(item['author']),
                                      ''.join(item['description'])))
            self.db.commit()
            self.count += 1
        except:
            print"insert fail"
        return item

    def spider_closed(self, spider):
        self.db.close()
        pass
