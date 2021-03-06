from rest_framework import serializers

from core.models import AssetData, Asset, Scraper


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = "__all__"


class AssetDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetData
        fields = "__all__"


class AssetDataListSerializer(serializers.Serializer):
    asset = serializers.CharField()
    values = AssetDataSerializer(many=True)


class ScraperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scraper
        fields = "__all__"
