from rest_framework import serializers

from .models import *


class AllBanksSerializer(serializers.ModelSerializer):

    class Meta:
        model = BankModel
        fields = ('id', 'name', 'logo',)


class BankModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = BankModel
        fields = ('id', 'name', 'logo', 'description',)


class BankBranchModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = BankBranchModel
        fields = ('id', 'name', 'address', 'phone', 'longitude', 'latitude',)


class BankContactsModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = BankContactsModel
        fields = ('id', 'type', 'data',)


class BankImagesModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = BankImagesModel
        fields = ('id', 'image',)


class ServicesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Services
        fields = ('id', 'name', 'logo')


class SuppliersModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Suppliers
        fields = ('id', 'name', 'logo',)


class SupplierTypeModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = SupplierTypeModel
        fields = ('id', 'name', 'logo', 'description',)


class SupplierBranchModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = SupplierBranchModel
        fields = ('id', 'name', 'address', 'phone', 'longitude', 'latitude',)


class SupplierContactsModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = SupplierContactsModel
        fields = ('id', 'type', 'data',)


class SupplierImagesModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = SupplierImagesModel
        fields = ('id', 'image',)
