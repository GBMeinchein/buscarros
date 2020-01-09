import scrapy

from buscarros.items import BuscarrosItem
from scrapy.http.request import Request

class WebmotorsSpider(scrapy.Spider):
    name = 'Webmotors'
    allowed_domains = ['webmotors.com.br']
    start_urls = ['https://www.webmotors.com.br/carros/sc/fiat?estadocidade=Santa%20Catarina&tipoveiculo=carros&marca1=FIAT']

    def start_requests(self):
        headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            yield Request(url, headers=headers)

    def parse(self, response):
        titles = response.css('h2.CardVehicle__details__header__title::text').extract()
        hrefs = response.css('a.CardVehicle__link::attr(href)').extract()
        # prices = response.css('p.OLXad-list-price::text').extract()
        # images = response.css('img.image.lazy::attr(data-original)').extract()
        # adresses = response.css('p.text.detail-region::text').extract()

        for item in zip(titles, hrefs):

            new_item = BuscarrosItem()

            new_item['title'] = item[0]
            new_item['href'] = item[1]
            new_item['price'] = item[2]
            # new_item['image'] = item[3]
            # new_item['adress'] = item[4]

            yield new_item
        
        #next_page = response.css('li.item.next').css('a.link::attr(href)').extract()[0]

        #yield Request(url=next_page, callback=self.parse)