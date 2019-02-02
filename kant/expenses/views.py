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
from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response


class ExpensesView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request, *args, **kwargs):
        # language = request.META.get('HTTP_LANGUAGE')
        # language_activate
        # print(kwargs)
        field_id = self.kwargs.get('field_id')
        print(field_id)

        if field_id is not None:
            field_expense = FieldExpenses.objects.filter(field_id=field_id)
            if len(field_expense) > 0:
                field_expense_serializer = FieldExpensesSerializer(field_expense, many=True)
                return Response(field_expense_serializer.data, status=status.HTTP_200_OK)
            return Response([],
                            status=status.HTTP_200_OK)

        expenses = Expenses.objects.all()
        # print(expenses)
        if len(expenses) > 0:
            expenses_serializer = ExpensesSerializer(expenses, many=True)
            return Response(expenses_serializer.data, status=status.HTTP_200_OK)
        return Response([],
                        status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        try:
            field_id = self.kwargs.get('field_id')
            # print(field_id)
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
                        expense_serializer.save()
                        return Response({'success': "Successfully changed."},
                                        status=status.HTTP_202_ACCEPTED)
                except:
                    return Response({"error": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response({'error': 'Uncaught internal server error.'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FieldsView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request, *args, **kwargs):
        # language = request.META.get('HTTP_LANGUAGE')
        # language_activate(request, language)
        try:
            user_id = self.kwargs.get('user_id')
            # print(user_id)
            fields = FieldsModel.objects.filter(user_id=user_id, ).order_by('year', '-id')
            if len(fields) > 0:
                fields_serializer = FieldsModelSerializer(fields, many=True)
                result = {
                    "all_fields": []
                }
                field = {}
                year = fields_serializer.data[0]['year']
                field_data = fields.filter(year=year)
                year_data = {}
                while len(fields) > 0:
                    json_data = FieldsModelSerializer(field_data, many=True)
                    print(json_data)
                    year_data['year'] = year
                    year_data['data'] = []

                    for item in json_data.data:
                        coord = CoordinatesModel.objects.filter(field_id=item['id'])
                        coord_data = CoordinateModelSerializer(coord, many=True, )
                        print('===========')
                        print(coord_data)
                        field_expenses = FieldExpenses.objects.filter(field_id=item['id'])
                        field_expenses_serializer = FieldExpensesSerializer(field_expenses, many=True, )
                        field['id'] = item['id']
                        field['point_name'] = SugarBeetPointModel.objects.get(pk=item['beet_point']).name
                        field['field_id'] = item['field_id']
                        field['hectares'] = item['hectares']
                        field['average_harvest'] = item['average_harvest']
                        field['coordinates'] = coord_data.data
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
            return Response([],
                            status=status.HTTP_200_OK)
        except FieldsModel.DoesNotExist:
            return Response([],
                            status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            user_id = self.kwargs.get('user_id')
            year = data['year']
            point_id = data['point_id']
            field_id = data['field_id']
            hectares = data['hectares']
            average_harvest = data['average_harvest']
            coordinates = data['coordinates']
        except KeyError:
            return Response({"error": "Database error"}, status=status.HTTP_400_BAD_REQUEST)
        # transaction.atomic() -> doesn't save automatically to db
        try:
            with transaction.atomic():
                field = FieldsModel(user_id=user_id, year=year,
                                    beet_point_id=point_id,
                                    field_id=field_id, hectares=hectares,
                                    average_harvest=average_harvest)

                field.save()
                if field:
                    field_pk = field.pk
                    for item in coordinates:
                        coor = CoordinatesModel(field=field,
                                                latitude=item['latitude'],
                                                longitude=item['longitude'],
                                                number=item['number'], )
                        coor.save()

                expenses = Expenses.objects.all()
                expenses_serializer = ExpensesSerializer(expenses, many=True)
                expense_data = {}
                expense_array = []
                for item in expenses_serializer.data:
                    field_expense = FieldExpenses(field=field,
                                                  name=item['name'],
                                                  price=item['price'], )
                    field_expense.save()
                    expense_data['id'] = field_expense.pk
                    expense_data['name'] = field_expense.name
                    expense_data['price'] = field_expense.price
                    expense_data['amount'] = field_expense.amount

                    expense_array.append(expense_data)
                result = {
                    "field_id": field_pk,
                    "expenses": expense_array
                }
                return Response(result, status=status.HTTP_201_CREATED)
        except DatabaseError:
            return Response({"error": "Database error"},
                            status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        try:
            field_id = self.kwargs.get('user_id')
            field = FieldsModel.objects.get(pk=field_id)
            field_serializer = FieldsModelSerializer(field,
                                                     data=request.data,
                                                     partial=True, )
            if field_serializer.is_valid():
                field_serializer.save()
                return Response(field_serializer.data,
                                status=status.HTTP_202_ACCEPTED)
            return Response({"error": "Bad request data."},
                            status=status.HTTP_400_BAD_REQUEST)
        except FieldsModel.DoesNotExist:
            return Response({"error": "Field with given ID not found."},
                            status=status.HTTP_404_NOT_FOUND)
        except KeyError:
            return Response({"error": "Key error occured. Please enter valid Keys"},
                            status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error": "Uncaught internal server error."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, **kwargs):
        try:
            field_id = self.kwargs.get('user_id')
            FieldsModel.objects.get(pk=field_id).delete()
            return Response({"success": "Field was deleted."},
                            status=status.HTTP_200_OK)
        except FieldsModel.DoesNotExist:
            return Response({"error": "Field with given ID not found."},
                            status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({"error": "Uncaught internal server error."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SugarBeetPointView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request, *args, **kwargs):
        try:
            sugar_beet_points = SugarBeetPointModel.objects.all()
            sugar_beet_points_serialzer = SugarBeetPointSerializer(sugar_beet_points, many=True )

            return Response(sugar_beet_points_serialzer.data, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Server internal error. "},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
