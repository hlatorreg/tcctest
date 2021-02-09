import time
import logging
import datetime
from scrapy import signals, Request, Spider
from core.models import Scraper, AssetData


class AssetsSpider(Spider):
    name = "assets"
    allowed_domains = ["www.coindesk.com"]

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        cls.scraper_id = kwargs.get("scraper_id")
        spider = super(AssetsSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_idle, signals.spider_idle)
        return spider

    def spider_idle(self, spider):
        scraper = Scraper.objects.filter(pk=self.scraper_id).get()
        time.sleep(scraper.scrape_frecuency)
        logging.info(f"starting a crawl again! for {scraper.url}")
        self.crawler.engine.schedule(
            Request(
                scraper.url, dont_filter=True, cb_kwargs=dict(asset_id=scraper.asset.pk)
            ),
            spider,
        )
        raise DontCloseSpider

    def parse(self, response, asset_id):
        price = response.xpath('//div[@class="price-large"]/text()').get()
        price_low = response.xpath(
            """//*[@id="__next"]/div[2]/main/section/div[2]/div[1]/div/section/div
            /div[3]/div/div[2]/div[1]/div[2]/div/text()"""
        ).get()
        price_high = response.xpath(
            """//*[@id="__next"]/div[2]/main/section/div[2]/div[1]/div/section/div
            /div[3]/div/div[2]/div[2]/div[2]/div/text()"""
        ).get()
        returns_24 = response.xpath(
            """//*[@id="__next"]/div[2]/main/section/div[2]
            /div[1]/div/section/div/div[3]/div/div[3]/div[3]
            /div[2]/div/span/span[1]/text()"""
        ).get()
        returns_ytd = response.xpath(
            """//*[@id="__next"]/div[2]/main/section/div[2]
            /div[1]/div/section/div/div[3]/div/div[3]/div[4]
            /div[2]/div/span/span[1]/text()"""
        ).get()
        volatility = response.xpath(
            """//*[@id="__next"]/div[2]/main/section/div[2]
            /div[1]/div/section/div/div[3]/div/div[3]/div[5]
            /div[2]/div/text()"""
        ).get()
        AssetData.objects.create(
            price=self._parse_floats(price),
            low_24h=self._parse_floats(price_low),
            high_24h=self._parse_floats(price_high),
            retunrs_24h=self._parse_floats(returns_24),
            retunrs_ytd=self._parse_floats(returns_ytd),
            volatility=self._parse_floats(volatility),
            asset_id=asset_id,
            data_datetime=datetime.datetime.now(),
        )

    def errback_httpbin(self, response):
        print("errback")
        print(response)
        pass

    def _parse_floats(self, value):
        removable = "$,"

        return float(value.translate({ord(c): None for c in removable}))
