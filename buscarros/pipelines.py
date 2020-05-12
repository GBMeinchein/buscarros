import pymongo

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log

class BuscarrosPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            itemSaved = self.collection.find_one({'href': item['href']})

            if itemSaved is None:
                self.collection.insert(dict(item))
            log.msg("Carros adicionados ao mongodb!",
                    level=log.DEBUG, spider=spider)
        return item   
