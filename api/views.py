import json
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from core.models import Asset, AssetData, Scraper
from api.serializers import (
    AssetSerializer,
    AssetDataSerializer,
    ScraperSerializer,
    AssetDataListSerializer,
)


class AssetAPIView(generics.ListCreateAPIView):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer


class UpdateAssetAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer


class AssetDataAPIView(generics.ListAPIView):
    queryset = AssetData.objects.all()
    serializer_class = AssetDataSerializer


class AssetDataByAssetAPIView(generics.GenericAPIView):
    def get(self, request, asset_name):
        print(asset_name)
        response = {
            "asset": asset_name,
            "values": AssetData.objects.order_by("creation_date").filter(
                asset__name=asset_name
            )[:30],
        }
        return Response(AssetDataListSerializer(response).data)


class ScraperAPIView(generics.ListCreateAPIView):
    queryset = Scraper.objects.all()
    serializer_class = ScraperSerializer


class UpdateScraperAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Scraper.objects.all()
    serializer_class = ScraperSerializer
