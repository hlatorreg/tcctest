import scrapy

from core.models import Scraper

class AssetsSpider(scrapy.Spider):
    name = 'assets'

    def start_requests(self):
        scraper = Scraper.objects.all()

        urls = [s.url for s in scraper]

        for u in urls:
            yield scrapy.Request(url=u, callback=self.parse)

    def parse(self, response):
        print(response.body)