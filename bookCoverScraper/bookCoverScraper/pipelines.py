# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
import requests

class BookcoverscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        imageDir = "./images/"
        url = "http://books.toscrape.com/" + adapter["imageUrl"].replace("..", "")
        fileName = imageDir + adapter["title"] + ".jpg"

        if not os.path.exists(imageDir):
            os.mkdir(imageDir)

        if not os.path.exists(fileName):
            with open(fileName, "wb") as f:
                data = requests.get(url).content
                f.write(data)

        return item
