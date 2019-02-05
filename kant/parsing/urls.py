from django.contrib import admin
from django.urls import path, include

from .views import (ScrapedSugarAndJomView,
                    NewsView,
                    WeatherFetchView,
                    AccuWeatherFetchView,
                    WeatherView)

app_name = "parsing"

urlpatterns = [
    path('sugar-jom/', ScrapedSugarAndJomView.as_view(), name='sugar-jom-view'),
    path('news/rossahar/', NewsView.as_view(), name='news-view'),
    path('fetch-weather/', WeatherFetchView.as_view(), name='fetch-weather-view'),
    path('weather/', WeatherView.as_view(), name='weather-view'),
    path('accu/', AccuWeatherFetchView.as_view(), name='accu-weather'),

]