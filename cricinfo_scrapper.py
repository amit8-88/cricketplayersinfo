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

    def parse(self, response):
        sel = Selector(text=response.body_as_unicode(), type="html")
        players_urlpath=sel.xpath(
            '//div[@id="ciPlayerbyCharAtoZ"]//ul//li//a/@href'
        )
        for url in players_urlpath.extract()[1:-1]:
            url = "http://www.espncricinfo.com" + url
            request = scrapy.Request(url, self.parse_player_names)
            yield request

    def parse_player_names(self,response):
        sel= Selector(text=response.body_as_unicode(), type="html")
        urlPath=sel.xpath(
            '//td[@class="ciPlayernames"]//a/@href'
        )

        for url in urlPath.extract()[1:-1]:
            url = "http://www.espncricinfo.com" + url
            request = scrapy.Request(url, self.parse_player_details)
            request.meta['url']=url
            yield request

    def parse_player_details(self, response):
        sel = Selector(text=response.body_as_unicode(), type="html")
        name = sel.xpath(
            '//div[@class="ciPlayernametxt"]/div/h1/text()'
        )

        dob_place=sel.xpath(
            '//p[@class="ciPlayerinformationtxt"]/b[contains(text(), "Born")]/following-sibling::span/text()'
        )

        teams=sel.xpath(
            '//p[@class="ciPlayerinformationtxt"]/b[contains(text(), "Major teams")]/following-sibling::span/text()'
        )



        yield {
            "name": name.extract()[0],
            "url": response.meta['url'],
            "born": dob_place.extract()[0],
            "teams": teams.extract()[0]

        }