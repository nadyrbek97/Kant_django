from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy

from .models import (Services,
                     BankModel,
                     BankBranchModel,
                     BankContactsModel,
                     BankImagesModel,
                     Suppliers,
                     SupplierBranchModel,
                     SupplierContactsModel,
                     SupplierImagesModel,
                     SupplierTypeModel,
                     TechnologyModel,
                     ContractsModel,
                     )

from users.models import *


# @admin.register(BankModel, BankContactsModel, BankImagesModel)
# class BankBranchModelAdmin(admin.ModelAdmin):
#     list_filter = ('bank', )


# Bank admin register with its Branches, Images, Contacts

class BankBranchInline(admin.StackedInline):
    exclude = ('name', 'address', )
    model = BankBranchModel
    fk_name = 'bank'
    extra = 1
    inlines = []


class BankImagesInline(admin.TabularInline):
    model = BankImagesModel
    extra = 0
    inlines = []


class BankContactsInline(admin.TabularInline):
    model = BankContactsModel
    extra = 0
    inlines = []


@admin.register(BankModel)
class BankAdmin(admin.ModelAdmin):
    list_filter = ('service',)
    exclude = ('name', 'description',)
    inlines = [BankBranchInline, BankContactsInline, BankImagesInline, ]
    # Bank admin register with its Branches, Images, Contacts


# Supplier admin register with its Branches, Images, Contacts
class SupplierBranchInline(admin.StackedInline):
    exclude = ('name', 'address',)
    model = SupplierBranchModel
    fk_name = 'supplier_type'
    extra = 0
    inlines =[]


class SupplierImagesInline(admin.TabularInline):
    model = SupplierImagesModel
    extra = 0
    inlines = []


class SupplierContactsInline(admin.TabularInline):
    model = SupplierContactsModel
    extra = 0
    inlines = []


@admin.register(SupplierTypeModel)
class SupplierAdmin(admin.ModelAdmin):
    # exclude = ('name', 'description',)
    inlines = [SupplierBranchInline, SupplierContactsInline, SupplierImagesInline, ]
    #  Supplier admin register with its Branches, Images, Contacts


@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    # exclude = ('name',)
    pass

@admin.register(Suppliers)
class SuppliersAdmin(admin.ModelAdmin):
    # exclude = ('name',)
    pass

