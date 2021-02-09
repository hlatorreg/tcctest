import datetime
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import Scraper, AssetData, Asset
from api.serializers import AssetSerializer, AssetDataSerializer
from django.urls import reverse


class ScraperAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.assets = [Asset.objects.create() for _ in range(3)]
        cls.asset = cls.assets[0]

        cls.assetsdata = [
            AssetData.objects.create(
                price=1.1,
                low_24h=1.1,
                high_24h=1.1,
                retunrs_24h=1.1,
                retunrs_ytd=1.1,
                volatility=1.1,
                data_datetime=datetime.datetime.now(),
                asset=cls.asset,
            )
            for _ in range(3)
        ]
        cls.assetdata = cls.assetsdata[0]

    def test_list_assets(self):
        response = self.client.get(reverse("asset-list"))
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(len(self.assets), len(response.data))

        for asset in self.assets:
            self.assertIn(AssetSerializer(instance=asset).data, response.data)

    def test_list_assets_data(self):
        response = self.client.get(reverse("asset-data-list"))
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(len(self.assets), len(response.data))

        for assetdata in self.assetsdata:
            self.assertIn(AssetDataSerializer(instance=assetdata).data, response.data)
