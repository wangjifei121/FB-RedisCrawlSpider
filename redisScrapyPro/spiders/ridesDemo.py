# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider
from redisScrapyPro.items import RedisscrapyproItem


class RidesdemoSpider(RedisCrawlSpider):
    name = 'ridesDemo'

    # scrapy_redis的调度器队列的名称，最终我们会根据该队列的名称向调度器队列中扔一个起始url
    redis_key = "redisQueue"

    link = LinkExtractor(allow=r'https://dig.chouti.com/.*?/.*?/.*?/\d+')
    link1 = LinkExtractor(allow=r'https://dig.chouti.com/all/hot/recent/1')
    rules = (
        Rule(link, callback='parse_item', follow=True),
        Rule(link1, callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        div_list = response.xpath('//*[@id="content-list"]/div')
        for div in div_list:
            content = div.xpath('string(./div[@class="news-content"]/div[1]/a[1])').extract_first().strip().replace("\t","")
            print(content)
            item = RedisscrapyproItem()
            item['content'] = content
            yield item
