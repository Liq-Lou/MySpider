# -*- coding: utf-8 -*-
import scrapy
from ..items import YanreItem

class Spider1Spider(scrapy.Spider):
    name = 'moe'
    allowed_domains = ['005.tv']
    start_urls = ['http://moe.005.tv/moeimg/tb/']

    def parse(self, response):
        url_list = response.xpath('//div[@class="zhuti_w_list"]/ul/li/a/@href').getall()
        for eve_url in url_list:
            yield scrapy.Request(eve_url, callback=self.parse_url)
        next_url_list = response.xpath('//div[@class="dede_pages"]/ul/a/@href').getall()
        for next_url in next_url_list:
            yield scrapy.Request(response.urljoin(next_url), callback=self.parse)

    def parse_url(self, response):
        img_url_list = response.xpath('//div[@class="content_nr"]/div/img/@src').getall()
        for img_url in img_url_list:
            yield YanreItem(img_url=[img_url])
        next_page_list = response.xpath('//div[@class="dede_pages"]/ul/a/@href').getall()
        for next_page in next_page_list:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse_url)
