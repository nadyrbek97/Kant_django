from django.shortcuts import render

from .models import *
from .serializers import *

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.generics import GenericAPIView


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
