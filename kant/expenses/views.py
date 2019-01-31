from django.shortcuts import render
from django.db import (transaction,
                       DatabaseError,
                       IntegrityError)

from .models import (Expenses,
                     FieldsModel,
                     FieldExpenses,
                     SugarBeetPointModel,
                     CommodityModel,
                     CoordinatesModel)

from .serializers import (ExpensesSerializer,
                          FieldExpensesSerializer,
                          FieldsModelSerializer,
                          SugarBeetPointSerializer,
                          CoordinateModelSerializer
                          )

from rest_framework.views import APIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response


class ExpensesView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        # language = request.META.get('HTTP_LANGUAGE')
        # language_activate
        print(kwargs)
        field_id = self.kwargs.get('field_id')
        if field_id is not None:
            field_expense = FieldExpenses.objects.filter(field_id=field_id)
            if len(field_expense) > 0:
                field_expense_serializer = FieldExpensesSerializer(field_expense, many=True)
                return Response(field_expense_serializer.data, status=status.HTTP_200_OK)
            return Response([],
                            status=status.HTTP_200_OK)

        expenses = Expenses.objects.all()
        if len(expenses) > 0:
            expenses_serializer = ExpensesSerializer(expenses, many=True)
            return Response(expenses_serializer.data, status=status.HTTP_200_OK)
        return Response([],
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            field_id = self.kwargs.get('field_id')
            expenses = request.data['expenses']
            with transaction.atomic():
                for item in expenses:
                    expense = FieldExpenses(field_id=field_id,
                                            name=item['name'],
                                            price=item['price'],
                                            amount=item['amount'], )
                    expense.save()
            return Response({"success": "Expenses added to the given field."},
                            status=status.HTTP_201_CREATED)
        except DatabaseError:
            return Response({"error": "Bad request"},
                            status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error": "Internal Server Error."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, *args, **kwargs):
        try:
            expenses = request.data['data']
            for item in expenses:
                try:
                    expense_id = item['id']
                    data = {
                        'price': item['price'],
                        'amount': item['amount']
                    }

                    expense = FieldExpenses.objects.filter(pk=expense_id)
                    expense_serializer = FieldExpensesSerializer(expense,
                                                                 data=data,
                                                                 partial=True, )
                    if expense_serializer.is_valid():
                        expense_serializer.save
                except:
                    pass
            return Response({'success': "Successfully changed."},
                            status=status.HTTP_202_ACCEPTED)
        except:
            Response({'error': 'Uncaught internal server error.'},
                     status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FieldsView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        # language = request.META.get('HTTP_LANGUAGE')
        # language_activate(request, language)
        try:
            user_id = kwargs.get('user_id')
            fields = FieldsModel.objects.filter(user_id=user_id, ).order_by('year', '-id')

            if len(fields) > 0:
                fields_serializer = FieldsModelSerializer(fields, many=True)
                result = {
                    "all_fields" : []
                }
                field = {}
                year = fields_serializer.data[0]['year']
                field_data = fields.filter(year=year)
                year_data = {}
                while len(fields) > 0:
                    json_data = FieldsModelSerializer(field_data, many=True)
                    year_data['year'] = year
                    year_data['data'] = []

                    for item in json_data.data:
                        coordinates = CoordinatesModel.objects.filter(field_id=item['id'])
                        coordinate_data = CoordinateModelSerializer(coordinates, many=True)
                        field_expenses = FieldExpenses.objects.filter(field_id=item['id'])
                        field_expenses_serializer = FieldExpensesSerializer(field_expenses, many=True)
                        field['id'] = item['id']
                        field['point_name'] = SugarBeetPointModel.objects.get(pk=item['beet_point']).name
                        field['field_id'] = item['field_id']
                        field['hectares'] = item['hectares']
                        field['average_harvest'] = item['average_harvest']
                        field['coordinates'] = coordinate_data.data
                        field['expenses'] = field_expenses_serializer.data
                        year_data['data'].append(field)
                        field = {}
                    result['all_fields'].append(year_data)
                    year_data = {}
                    fields = fields.filter(year__gt=year)
                    fields_serializer = FieldsModelSerializer(fields, many=True)
                    if len(fields) == 0:
                        break
                    year = fields_serializer.data[0]['year']
                    field_data = fields.filter(year=year)
                return Response(result, status=status.HTTP_200_OK)
            return Response([], status=status.HTTP_200_OK)
        except FieldsModel.DoesNotExist:
            return Response([], status=status.HTTP_200_OK)





