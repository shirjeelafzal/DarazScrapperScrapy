import scrapy


class CategoriesspiderSpider(scrapy.Spider):
    name = "categoriesspider"
    allowed_domains = ["www.daraz.pk"]
    start_urls = ["https://www.daraz.pk/"]

    def parse(self, response):
        pass
