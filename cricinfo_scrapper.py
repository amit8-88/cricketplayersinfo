import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re
import json
from pymongo import MongoClient
from scrapy.http import Request, FormRequest

class CricInfoScrapeSpider(scrapy.Spider):
    name='cricinfo-spider'
    start_urls=['http://www.espncricinfo.com/ci/content/player/country.html?country=6;alpha=A']

    def parse(self,response):
        sel=sel = Selector(text=response.body_as_unicode(), type="html")
        urlPath=sel.xpath(
            '//td[@class="ciPlayernames"]//a/@href'
        )
        # for url in urlPath.extract()[1:-1]:
        #     url = "http://www.espncricinfo.com" + url
        #     request = self.request(url, self.parse_player_name)
        for url in urlPath.extract()[1:-1]:
            url = "http://www.espncricinfo.com" + url
            request = scrapy.Request(url, self.parse_player_name)
            yield request


        #request = scrapy.Request(url, self.parse_reviewScore)


    def parse_player_name(self, response):
        sel = Selector(text=response.body_as_unicode(), type="html")
        urlPath = sel.xpath(
            '//div[@class="ciPlayernametxt"]/div/h1/text()'
        )

        yield {
            "player_name": urlPath.extract()[0]
        }