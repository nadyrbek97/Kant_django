from .serializers import *

from urllib.request import Request, urlopen

import json
import ssl

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.pagination import LimitOffsetPagination
from .models import WeatherModel
from .methods import (accuweather_five_day_result_process,
                      accuweather_one_day_result_process,
                      )


class CurrencyFetchView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        try:
            try:
                _create_unverified_https_context = ssl._create_unverified_context
            except AttributeError:
                # Legacy Python that doesn't verify HTTPS certificates by default
                pass
            else:
                # Handle target environment that doesn't support HTTPS verification
                ssl._create_default_https_context = _create_unverified_https_context
            req = Request('https://valuta.kg/api/rate/average.json')
            response_body = urlopen(req)
            data = response_body.read()
            encoding = response_body.info().get_content_charset('utf-8')
            result = json.loads(data.decode(encoding))
            if len(result) > 0:
                CurrencyModel.objects.all().delete()
                currency = CurrencyModel(data=result)
                currency.save()
                return Response({"success": "Success processing."},
                                status=status.HTTP_200_OK)
            return Response({"error": "Error occurred while processing."},
                            status=status.HTTP_501_NOT_IMPLEMENTED)
        except:
            return Response({"error": "Error while processing."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CurrencyView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        try:
            currency = CurrencyModel.objects.all()
            currency_serializer = CurrencyModelSerializer(currency, many=True, )
            result = {"data": currency_serializer.data[0]['data']['data']}
            return Response(result, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Error while processing."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WeatherFetchView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        # try:
        five_day_request = Request(
            'http://dataservice.accuweather.com/forecasts/v1/daily/5day/222844?apikey=xdAJQ1uN1QGBmqX3CmxG9otXhpefsTfG')
        five_day_response_body = urlopen(five_day_request)
        five_day_data = five_day_response_body.read()
        five_day_encoding = five_day_response_body.info().get_content_charset('utf-8')
        five_day_result = json.loads(five_day_data.decode(five_day_encoding))
        five_day = accuweather_five_day_result_process(five_day_result['DailyForecasts'])

        day_request = Request(
            'http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/222488?apikey=xdAJQ1uN1QGBmqX3CmxG9otXhpefsTfG')
        day_response_body = urlopen(day_request)
        day_data = day_response_body.read()
        day_encoding = day_response_body.info().get_content_charset('utf-8')
        day_result = json.loads(day_data.decode(day_encoding))
        one_day = accuweather_one_day_result_process(day_result)
        res = {
            "list": five_day,
            "today": one_day
        }
        if len(res) > 0:
            WeatherModel.objects.all().delete()
            weather = WeatherModel(data=res)
            weather.save()
            return Response({"success": "Success processing."},
                            status=status.HTTP_200_OK)
        return Response({"error": "Error occurred while processing."},
                        status=status.HTTP_501_NOT_IMPLEMENTED)


class AccuWeatherFetchView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        # try:
        five_day_request = Request(
            'http://dataservice.accuweather.com/forecasts/v1/daily/5day/222844?apikey=xdAJQ1uN1QGBmqX3CmxG9otXhpefsTfG')
        five_day_response_body = urlopen(five_day_request)
        five_day_data = five_day_response_body.read()
        five_day_encoding = five_day_response_body.info().get_content_charset('utf-8')
        five_day_result = json.loads(five_day_data.decode(five_day_encoding))
        five_day = accuweather_five_day_result_process(five_day_result['DailyForecasts'])

        day_request = Request(
            'http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/222488?apikey=xdAJQ1uN1QGBmqX3CmxG9otXhpefsTfG')
        day_response_body = urlopen(day_request)
        day_data = day_response_body.read()
        day_encoding = day_response_body.info().get_content_charset('utf-8')
        day_result = json.loads(day_data.decode(day_encoding))
        one_day = accuweather_one_day_result_process(day_result)

        res = {
            "list": five_day,
            "today": one_day
        }

        return Response(res, status=status.HTTP_200_OK)
        # if len(five_day_result) > 0:
        #     print('dddd')
        #     result_data = process_weather(five_day_result['list'])
        #     print('rrrr')
        #     WeatherModel.objects.all().delete()
        #     weather = WeatherModel(data=result_data)
        #     weather.save()
        #     return Response({"success": "Success processing."},
        #                     status=status.HTTP_200_OK)
        # return Response({"error": "Error occurred while processing."},
        #                 status=status.HTTP_501_NOT_IMPLEMENTED)
        # except:
        #      return Response({"error": "Error while processing."},
        #                      status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WeatherView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        try:
            weather = WeatherModel.objects.all()
            weather_serializer = WeatherModelSerializer(weather, many=True, )
            return Response(weather_serializer.data[0]['data'],
                            status=status.HTTP_200_OK)
        except:
            return Response({"error": "Error while processing."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ScrapedSugarAndJomView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        try:
            sugar = SugarModel.objects.all()
            sugar_serializer = SugarSerializer(sugar, many=True)

            jom = JomModel.objects.all()
            jom_serializer = JomSerializer(jom, many=True)
            result = {
                'sugar': sugar_serializer.data[-2:],
                'jom': jom_serializer.data[-2:]
            }

            return Response(result, status=status.HTTP_200_OK)
        except:
            return Response({"error": "No data found."},
                            status=status.HTTP_404_NOT_FOUND)


class NewsView(APIView):
    permission_classes = (permissions.AllowAny,)

    queryset = NewsModel.objects.all().order_by('-id')
    serializer_class = NewsModelSerializer
    pagination_class = LimitOffsetPagination

    def get(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.queryset)
        if len(page) > 0:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response([], status=status.HTTP_200_OK)

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)
