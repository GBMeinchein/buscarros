# # -*- coding: utf-8 -*-
# import scrapy


# class OlxSpider(scrapy.Spider):
#     name = 'Olx'
#     allowed_domains = ['olx.com.br']
#     start_urls = ['http://olx.com.br/']

#     def parse(self, response):
#         pass

# -*- coding: utf-8 -*-
import scrapy

from buscarros.items import BuscarrosItem
from scrapy.http.request import Request

class OlxSpider(scrapy.Spider):
    name = 'Olx'
    allowed_domains = ['olx.com.br']
    start_urls = ['https://sc.olx.com.br/florianopolis-e-regiao/grande-florianopolis/autos-e-pecas/carros-vans-e-utilitarios?ctp=1']

    def parse(self, response):
        titles = response.css('h2.OLXad-list-title::text').extract()
        hrefs = response.css('a.OLXad-list-link::attr(href)').extract()
        prices = response.css('p.OLXad-list-price::text').extract()

        for item in zip(titles, hrefs, prices):

            new_item = BuscarrosItem()

            new_item['title'] = item[0]
            new_item['href'] = item[1]
            new_item['price'] = item[2]

            yield new_item
        
        next_page = response.css('li.item.next').css('a.link::attr(href)').extract()[0]

        yield Request(url=next_page, callback=self.parse)