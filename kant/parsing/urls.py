from django.contrib import admin
from django.urls import path, include

from .views import (ScrapedSugarAndJomView,
                    NewsView)

urlpatterns = [
    path('sugar-jom/', ScrapedSugarAndJomView.as_view(), name='sugar-jom-view'),
    path('news/rossahar/', NewsView.as_view(), name='news-view')
]