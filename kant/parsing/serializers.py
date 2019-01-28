from rest_framework import serializers

from .models import (
    NewsModel,
    SugarModel,
    JomModel
)


class SugarSerializer(serializers.ModelSerializer):

    class Meta:
        model = SugarModel
        fields = ('name', 'date', 'price', 'percentage')


class JomSerializer(serializers.ModelSerializer):

    class Meta:
        model = JomModel
        fields = ('name', 'date', 'price', 'percentage')


class NewsModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewsModel
        fields = ('link', 'data', 'name', 'description',)

