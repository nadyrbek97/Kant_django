from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response

from .serializers import *
from .models import *


class BankView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, *args, **kwargs):

        bank_id = self.kwargs.get('bank_id')
        print(bank_id)

        if not bank_id:
            banks = BankModel.objects.all()
            banks_serializer = AllBanksSerializer(banks, many=True, )

            return Response(banks_serializer.data, status=status.HTTP_200_OK)

        try:
            bank = BankModel.objects.get(pk=bank_id)

            if bank:
                bank_serializer = BankModelSerializer(bank, many=False)
                print(bank_serializer.data)

                return Response(bank_serializer.data, status=status.HTTP_200_OK)
        except BankModel.DoesNotExist:
            return Response([], status=status.HTTP_200_OK)




