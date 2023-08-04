import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]

    custom_settings = {
            "FEEDS": {"data.jsonl": {"format": "jsonlines", "overwrite": True}}
            }

    def parse(self, response):
        books = response.css("article.product_pod")
        for book in books:
            yield {
                    "imageUrl": book.css("img.thumbnail").attrib["src"],
                    "title": book.css("h3 a::text").get()
                    }
        nextPage = None
        try: 
            nextPage = response.css("li.next a").attrib["href"]
        except:
            nextPage = None

        if nextPage is not None:
            if "catalogue" in nextPage:
                nextPageUrl = "http://books.toscrape.com/" + nextPage
            else:
                nextPageUrl = "http://books.toscrape.com/catalogue/" + nextPage
        
            yield response.follow(nextPageUrl, callback=self.parse)
