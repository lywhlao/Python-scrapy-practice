# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
import re

from kan.items import *


class DmozSpider(CrawlSpider):
    count = 1
    name = "kan"
    allowed_domains = ["kankindle.com"]
    start_urls = [
        "http://kankindle.com/"
    ]

    rules = (
        Rule(LinkExtractor(allow=('/simple/page/\d+',)), follow=True),
        Rule(LinkExtractor(allow=('/view/\d+\.html')), callback='parse_content', follow=False),
    )

    def parse_content(self, response):
        item = KanItem()
        item['book_title'] = self.getFileTitle(response)
        item['file_urls'] = self.getFileUrl(response)
        item['description'] = self.getFileDescription(response)
        item['author'] = self.getFileAuthor(response)
        return item

    # getFileTitle
    def getFileTitle(self, response):
        info_string_list = response.xpath('//div[@class="hero-unit"]/text()').extract()
        r = re.compile(u"[\w\W\u4e00-\u9fa5]+\.(mobi|azw3|txt|epub|pdf|MOBI|AZW3|TXT|EPUB|PDF)")
        file_title = "null"
        for temp in info_string_list:
            file_title_re = r.search(temp, re.IGNORECASE)  # ignoreCase
            if file_title_re is not None:
                file_title = file_title_re.group().replace(u"书籍名称：", "")
                break
        if file_title == 'null':
            file_title = response.xpath("//h1/text()").extract()
        file_title = re.sub(r"\r|\n", "", file_title)
        return file_title

    # getFileUrl
    def getFileUrl(self, response):
        link_list = response.xpath('//a/@href').re(r'http://kankindle.com/simple/down/\d+')
        link_list_pan = response.xpath('//a[contains(@href,"http://pan.baidu.com")]/@href').extract()
        if len(link_list) > 0:
            return link_list
        elif len(link_list_pan) > 0:
            return link_list_pan
        else:
            return 'null'

    # getFileDescription
    def getFileDescription(self, response):

        description = response.xpath('//div[@id="detail-tag-id-3"]//div[@class="book-detail-content"]/text()').extract()
        if len(description) == 0:
            description = response.xpath(
                '//div[@id="detail-tag-id-3"]//div[@class="book-detail-content"]//p/text()').extract()
        if len(description) == 0:
            description = response.xpath(
                '//div[@id="detail-tag-id-3"]//div[@class="book-detail-content"]/div/text()').extract()
        return description

    # getAuhtor
    def getFileAuthor(self, response):
        info_list = response.xpath('//div[@class="hero-unit"]/text()').extract()
        author = 'null'
        for temp in info_list:
            temp = temp.encode('utf-8')
            r = re.compile(r"(\,|mobi|azw3|本书作者|\：)")
            if temp.find('本书作者') > -1:
                author = re.sub(r, "", temp)
        author = re.sub(r"\r|\n", "", author)
        return author
