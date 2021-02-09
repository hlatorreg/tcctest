from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from scraper.scraper import settings as my_settings
from scraper.scraper.spiders.assets_spider import AssetsSpider
from core.models import Scraper


class Command(BaseCommand):
    help = "Release assets spider"

    def add_arguments(self, parser):
        parser.add_argument("-scraper", type=int)

    def handle(self, *args, **options):
        print(options)
        if options["scraper"] is None or options["scraper"] <= 0:
            raise CommandError("Invalid scraper id, indicate a valid scraper id")
        else:
            try:
                scraper = Scraper.objects.filter(
                    pk=options["scraper"], active=True
                ).get()
            except ObjectDoesNotExist:
                raise CommandError("No hay un scraper activo con ese identificador")
            c_settings = Settings()
            c_settings.setmodule(my_settings)
            process = CrawlerProcess(settings=c_settings)
            process.crawl(AssetsSpider, scraper_id=options["scraper"])
            process.start()
