import scrapy
from scrapy_splash import SplashRequest
class ForyouspiderSpider(scrapy.Spider):
    name = "foryouspider"
    allowed_domains = ["www.daraz.pk"]
    start_urls = ["https://www.daraz.pk/#hp-just-for-you"]
    def start_requests(self):
        url = "https://www.daraz.pk/#hp-just-for-you"
        yield SplashRequest(url=url,callback= self.parse, args={'wait': 10})
    

    def parse(self, response):
        cards = response.css('.card-jfy-item-wrapper')
        for card in cards:
            yield {
                'Product Name': card.css('.card-jfy-title .title::text').get(),
                'Discounted Price': f'{card.css('.hp-mod-price-first-line .currency::text').get().strip('.')}:{card.css('.hp-mod-price-first-line .price::text').get()}',
                'Original Price': f'{card.css('.hp-mod-price-first-line .currency::text').get().strip('.')}:{card.css('.hp-mod-price-second-line .price::text').get()}',
                'Discount': card.css('.hp-mod-price .hp-mod-price-second-line .hp-mod-discount::text').get(),
                'Comments Count': card.css('.card-jfy-footer .card-jfy-ratings-comment::text').get().strip('()'),
            }
    