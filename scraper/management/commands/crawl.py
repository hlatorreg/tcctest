from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from scraper.scraper import settings as my_settings
from scraper.scraper.spiders.assets_spider import AssetsSpider

class Command(BaseCommand):
    help = 'Release assets spider'

    def handle(self, *args, **options):
        c_settings = Settings()
        c_settings.setmodule(my_settings)
        process = CrawlerProcess(settings=c_settings)
        process.crawl(AssetsSpider)
        process.start()
