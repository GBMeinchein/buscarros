import scrapy
import json

from buscarros.items import BuscarrosItem
from scrapy.http.request import Request

class WebmotorsSpider(scrapy.Spider):
    name = 'Webmotors'
    allowed_domains = ['webmotors.com.br']
    start_urls = ['https://www.webmotors.com.br/api/search/car?url=https://www.webmotors.com.br/carros%2Fsc%2Ffiat%3Festadocidade%3DSanta%2520Catarina&actualPage=1&displayPerPage=24&order=1&showMenu=true&showCount=true&showBreadCrumb=true&testAB=false&returnUrl=false']#['https://www.webmotors.com.br/carros/sc/fiat?estadocidade=Santa%20Catarina&tipoveiculo=carros&marca1=FIAT']

    def start_requests(self):
        headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            yield Request(url, headers=headers)

    def parse(self, response):
        jsonresponse = json.loads(response.body)
        
        i = 0
        for SearchResult in jsonresponse["SearchResults"]:
            
            new_item = BuscarrosItem()          

            new_item['title'] = SearchResult["Specification"]["Title"]
            new_item['href'] = SearchResult["Specification"]["Title"]
            new_item['price'] = str(SearchResult["Prices"]["Price"])
            new_item['image'] = "https://image.webmotors.com.br/_fotos/anunciousados/gigante/" + SearchResult["Media"]["Photos"][0]["PhotoPath"]
            new_item['adress'] = SearchResult["Seller"]["City"]

            yield new_item
        
        #next_page = response.css('li.item.next').css('a.link::attr(href)').extract()[0]

        #yield Request(url=next_page, callback=self.parse)