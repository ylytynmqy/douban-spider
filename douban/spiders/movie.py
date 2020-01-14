# -*- coding: utf-8 -*-
import scrapy, json
from scrapy import Request, Selector
from douban.items import *
import logging


class MovieSpider(scrapy.Spider):
    name = "movie"
    film_listurl = 'https://movie.douban.com/j/new_search_subjects?sort=T&range=1,10&tags=%E7%94%B5%E5%BD%B1&start={page}&year_range=1,1995'
    film_url = 'https://movie.douban.com/subject/{id}/?apikey=0b2bdeda43b5688921839c8ecb20399b'
    def start_requests(self):
        for i in range(446,480):
            yield Request(self.film_listurl.format(page=(i * 20)), callback=self.parse)

    def parse(self, response):

        self.logger.debug(response)
        result = json.loads(response.text)
        if result.get('data'):
            filmlist = result.get('data')
            if filmlist:
                for film in filmlist:
                    # 获取电影id
                    id = film.get('id')
                    title = film.get('title')
                    logging.getLogger(__name__).debug("已获取电影id：%s %s" % (title, id))
                    # 已经爬好的id不再爬
                    yield Request(self.film_url.format(id=id), callback=self.parse_film, meta={'id': id})

    def parse_film(self, response):

        selector = Selector(response=response)
        # id
        id = response.meta.get('id')
        # 电影名字
        title = selector.xpath('//*[@id="content"]/h1/span[1]/text()').extract()
        # 年份
        year = str(selector.xpath('//*[@id="content"]/h1/span[2]/text()').extract())
        year=year[3:len(year)-3]
        year=int(year)
        # 评分
        try:
            rate = str(selector.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()').extract())
            rate=rate[2:len(rate)-2]
            rate=float(rate)
        except IndexError:
            rate = None
        # 评价人数
        try:
            rating_num = str(selector.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/div/div[2]/a/span/text()').extract())
            rating_num=rating_num[2:len(rating_num)-2]
            rating_num=int(rating_num)
        except IndexError:
            rating_num = None
        # 标签
        tags = response.css('div.tags-body a::text').getall()
        # 导演
        director = []
        for d in selector.xpath('//*[@id="info"]/span[1]/span[2]/a'):
            temp = d.xpath('text()').extract()
            director.append(temp)
        # 演员
        actor=response.css('.actor a::text').getall()
        film_info_item = DoubanItem()
        field_map = {
            'id': id, 'title': title, 'year': year, 'rate': rate, 'rating_num': rating_num, 'tags': tags,
            'director': director, 'actor': actor
        }

        for field, attr in field_map.items():
            film_info_item[field] = attr

        yield film_info_item
