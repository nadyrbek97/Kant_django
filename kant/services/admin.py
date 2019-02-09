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
from expenses.models import *
from expenses.serializers import (CoordinateModelSerializer,
                                  FieldsModelSerializer)


# admin.site.register(Services)
# admin.site.register(BankModel)
# admin.site.register(BankBranchModel)
# admin.site.register(BankContactsModel)
# admin.site.register(BankImagesModel)
# admin.site.register(Suppliers)
# admin.site.register(SupplierBranchModel)
# admin.site.register(SupplierImagesModel)
# admin.site.register(SupplierContactsModel)
# admin.site.register(SupplierTypeModel)
# admin.site.register(TechnologyModel)
# admin.site.register(ContractsModel)


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
    exclude = ('name', 'description',)
    inlines = [SupplierBranchInline, SupplierContactsInline, SupplierImagesInline, ]
    # Supplier admin register with its Branches, Images, Contacts


# Register Fields and its Coordinates
class CoordinatesInline(admin.TabularInline):
    model = CoordinatesModel
    extra = 0


class FieldExpensesInline(admin.TabularInline):
    model = FieldExpenses
    fk_name = 'field'
    extra = 0


from django.template.response import HttpResponse
from django.template import loader


def draw_map(modeladmin, request, queryset):
    template = loader.get_template('google_maps.html')
    import json
    context = {
        "fields": []
    }
    for item in queryset:
        f = FieldsModel.objects.get(pk=item.id)
        f_ser = FieldsModelSerializer(f, many=False)
        user = UserProfile.objects.get(user_id=item.user_id)
        beet_point = SugarBeetPointModel.objects.get(pk=item.beet_point.id)
        first_name = str(user.first_name)
        last_name = str(user.last_name)
        point_name = str(beet_point.name)
        field = {
            "longitude": [],
            "latitude": [],
            "average_harvest": f_ser.data['average_harvest'],
            "hectares": f_ser.data['hectares'],
            "year": f_ser.data['year'],
            "name": first_name,
            "last_name": last_name,
            "beet_point": point_name
        }
        coordinate = CoordinatesModel.objects.filter(field=item)
        coordinates_serializer = CoordinateModelSerializer(coordinate, many=True,)
        for i in coordinates_serializer.data:
            field['longitude'].append(i['longitude'])
            field['latitude'].append(i['latitude'])

        context['fields'].append(field)

    return HttpResponse(template.render(context))
draw_map.short_description = 'Нарисовать поля'


@admin.register(FieldsModel)
class FieldsAdmin(admin.ModelAdmin):
    inlines = [CoordinatesInline, FieldExpensesInline, ]
    list_filter = ('beet_point', 'year',)
    list_display = ('user', 'user_name', 'beet_point', 'year', 'average_harvest',
                    'hectares',)

    actions = [draw_map,]

    def user_name(self, obj):
        us = UserProfile.objects.get(user=obj.user_id)
        return "{} {}".format(us.first_name, us.last_name)
    user_name.short_description = "Имя и Фамилия"


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'email', 'city',)
    #change_form_template = '/Users/mamur/Documents/code/django/kndk/kndk/bank/templates/userprofile_admin.html'
    # exclude = ('firebase_token',)


@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    exclude = ('name',)


@admin.register(Suppliers)
class SuppliersAdmin(admin.ModelAdmin):
    exclude = ('name',)


@admin.register(Expenses)
class ExpensesModelTranslation(admin.ModelAdmin):
    exclude = ('name',)


@admin.register(SugarBeetPointModel)
class SugarBeetPointAdmin(admin.ModelAdmin):
    exclude = ('name',)
