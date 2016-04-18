from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

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
        item['book_title'] = response.xpath("//h1/text()").extract()
        link_list = response.xpath('//a/@href').re(r'http://kankindle.com/simple/down/\d+')
        link_list_pan = response.xpath('//a[contains(@href,"http://pan.baidu.com")]/@href').extract()
        if len(link_list) > 0:
            item['file_urls'] = link_list[0]
        elif len(link_list_pan) > 0:
            item['file_urls'] = link_list_pan[0]
        else:
            item['file_urls'] = 'null'
        return item
