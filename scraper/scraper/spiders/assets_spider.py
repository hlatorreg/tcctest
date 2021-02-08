import scrapy
import datetime
from core.models import Scraper, AssetData


class AssetsSpider(scrapy.Spider):
    name = "assets"

    def start_requests(self):
        scraper = Scraper.objects.all()

        urls = [(s.url, s.asset_id) for s in scraper]

        for s in scraper:
            s.last_update = datetime.datetime.now()
            s.save()

        for u in urls:
            yield scrapy.Request(
                url=u[0], callback=self.parse, cb_kwargs=dict(asset_id=u[1])
            )

    def parse(self, response, asset_id):
        from scrapy.shell import inspect_response

        # inspect_response(response, self)
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
        print(
            f"""price: {self._parse_floats(price)},
            price_low: {self._parse_floats(price_low)},
            price_high: {self._parse_floats(price_high)},
            returns_24: {self._parse_floats(returns_24)},
            returns_ytd: {self._parse_floats(returns_ytd)},
            volatility: {self._parse_floats(volatility)},
            asset_id: {asset_id},"""
        )
        AssetData.objects.create(
            price=self._parse_floats(price),
            low_24h=self._parse_floats(price_low),
            high_24h=self._parse_floats(price_high),
            retunrs_24h=self._parse_floats(returns_24),
            retunrs_ytd=self._parse_floats(returns_ytd),
            volatility=self._parse_floats(volatility),
            asset_id=asset_id,
            data_datetime=datetime.datetime.now()
        )

    def _parse_floats(self, value):
        removable = '$,'
        
        return float(value.translate({ord(c): None for c in removable}))