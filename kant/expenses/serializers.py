from rest_framework import serializers

from .models import (FieldsModel,
                     FieldExpenses,
                     SugarBeetPointModel,
                     Expenses,
                     CoordinatesModel)


class FieldsModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = FieldsModel
        fields = ('beet_point', 'id', 'year', 'average_harvest', 'field_id', 'hectares', )


class ExpensesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expenses
        fields = ('id', 'name', 'price', 'amount')


class FieldExpensesSerializer(serializers.ModelSerializer):

    class Meta:
        model = FieldExpenses
        fields = ('id', 'name', 'price', 'amount')


class SugarBeetPointSerializer(serializers.ModelSerializer):

    class Meta:
        model = SugarBeetPointModel
        fields = ('id', 'name')


class CoordinateModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = CoordinatesModel
        fields = ('longitude', 'latitude', 'number')

