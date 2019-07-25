# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
import re
from ArticleSpider.items import ArticleItem

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com/']
    start_urls = ['https://movie.douban.com/review/best/']

    def parse(self, response):
        # movie_name = response.css('.review-list.chart .subject-img img::attr(title)').extract()
        # image_src = response.css('.review-list.chart .subject-img img::attr(src)').extract()
        # url = response.css('.review-list.chart .subject-img::attr(href)').extract()
        # user_name = response.css('.review-list.chart .name::text').extract()
        # start = response.css('.review-list.chart span[class*="main-title-rating"]::attr(title)').extract()
        # date = response.css('.review-list.chart .main-meta::text').extract()

        list = response.css('.review-list.chart div[data-cid]')
        for div in list:
            img_src = div.css('a.subject-img img::attr(src)').extract_first()
            post_url = div.css('h2 a::attr(href)').extract_first()
            movie_url = div.css('.subject-img::attr(href)').extract_first()
            meta = {
                'img_url': img_src,
                'movie_url': movie_url
            }
            yield Request(url=parse.urljoin(response.url, post_url),meta=meta, callback=self.detail_parse,
                          dont_filter=True)

        next_page = response.css('.next > a:nth-child(2)::attr(href)').extract_first()
        yield Request(url=parse.urljoin(response.url, next_page), callback=self.parse, dont_filter=True)

    def detail_parse(self,response):
        # 实例化ArticleItem
        article_item = ArticleItem()
        name = response.xpath('/html/body/div[3]/div[1]/div/div[1]/div[1]/div/header/a[1]/span/text()').extract_first()
        name = ''.join(name)
        title = response.xpath('/html/body/div[3]/div[1]/div/div[1]/h1/span/text()').extract()
        title = ''.join(title)
        star = response.xpath('/html/body/div[3]/div[1]/div/div[1]/div[1]/div/header/span[1]/@title').extract_first()
        star = ''.join(star)
        date = response.css('.main-meta::text').extract_first()
        date = ''.join(date)
        movie_name = response.xpath('/html/body/div[3]/div[1]/div/div[1]/div[1]/div/header/a[2]/text()').extract_first()
        movie_name = ''.join(movie_name)
        text = str(response.css('.review-content *').extract())
        support_nums = response.css('button.btn:nth-child(1)::text').extract_first().strip()
        re_match = re.search("/d+", support_nums)
        if re_match:
            support = re_match.group()
        else:
            support = 0
        opposes = response.css('button.btn:nth-child(2)::text').extract_first().strip()
        re_match2 = re.search("/d+", opposes)
        if re_match2:
            oppose = re_match.group()
        else:
            oppose = 0
        img_url = response.meta.get('img_url', '')
        movie_url = response.meta.get('movie_url', '')

        article_item['name'] = name
        article_item['title'] = title
        article_item['star'] = star
        article_item['date'] = date
        article_item['movie_name'] = movie_name
        article_item['text'] = text
        article_item['support'] = support
        article_item['oppose'] = oppose
        article_item['img_url'] = [img_url]
        article_item['movie_url'] = movie_url
        yield article_item








