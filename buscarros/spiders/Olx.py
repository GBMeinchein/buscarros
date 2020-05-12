# -*- coding: utf-8 -*-
import scrapy
import re

from scrapy import log

from buscarros.items import BuscarrosItem
from scrapy.http.request import Request

class OlxSpider(scrapy.Spider):
    name = 'Olx'
    allowed_domains = ['olx.com.br']
    start_urls = ['https://sc.olx.com.br/florianopolis-e-regiao/grande-florianopolis/autos-e-pecas/carros-vans-e-utilitarios/fiat?ctp=1']
    #start_urls = ['https://sc.olx.com.br/florianopolis-e-regiao/grande-florianopolis/autos-e-pecas/carros-vans-e-utilitarios/gm-chevrolet?ctp=1']

    def start_requests(self):
        headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            yield Request(url, headers=headers)

    def parse(self, response):
        titles = response.css('h2.fnmrjs-10::text').extract()
        hrefs = response.css('a.fnmrjs-0::attr(href)').extract()
        prices = response.css('p.fnmrjs-16::text').extract()
        images = response.css('img.sc-1q8ortj-1::attr(src)').extract()
        adresses = response.css('p.fnmrjs-13::text').extract()

        for item in zip(titles, hrefs, prices, images, adresses):

            new_item = BuscarrosItem()

            new_item['title'] = item[0].strip()
            new_item['href'] = item[1].strip()
            new_item['price'] = float(re.sub('[^0-9]','', item[2].strip()))
            new_item['image'] = item[3].strip()
            new_item['adress'] = item[4].strip().split(", ")[0]
            new_item['site'] = 'OLX'
            new_item['brand'] = 'GM'

            yield new_item
        
        next_page = response.css('li.sc-1m4ygug-0.ilgdSS').css('a.sc-1m4ygug-2::attr(href)').extract()[0]

        yield Request(url=next_page, callback=self.parse)