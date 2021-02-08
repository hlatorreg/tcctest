from django.shortcuts import render
from rest_framework import generics
from core.models import Asset, AssetData, Scraper
from api.serializers import AssetSerializer, AssetDataSerializer, ScraperSerializer


class AssetAPIView(generics.ListCreateAPIView):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer


class AssetDataAPIView(generics.ListCreateAPIView):
    queryset = AssetData.objects.all()
    serializer_class = AssetDataSerializer


class AssetDataByAssetAPIView(generics.ListAPIView):
    serializer_class = AssetDataSerializer

    def get_queryset(self):
        asset_name = self.kwargs["asset_name"]
        return AssetData.objects.filter(asset__name=asset_name)


class ScraperAPIView(generics.ListCreateAPIView):
    queryset = Scraper.objects.all()
    serializer_class = ScraperSerializer


# Create your views here.
