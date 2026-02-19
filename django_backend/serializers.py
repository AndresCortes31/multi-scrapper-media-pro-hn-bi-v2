
from rest_framework import serializers
from .models import ScrapeResult, ScraperKey

class ScrapeResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapeResult
        fields = '__all__'

class ScraperKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = ScraperKey
        fields = ['platform', 'purpose', 'is_active', 'last_used']
