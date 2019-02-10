from django.contrib import admin
from users.models import UserProfile

from .models import (Expenses,
                     FieldsModel,
                     SugarBeetPointModel,
                     FieldExpenses,
                     CoordinatesModel
                     )
from .serializers import (CoordinateModelSerializer,
                          FieldsModelSerializer,
                          )

from django.template.response import HttpResponse
from django.template import loader


# Register Fields and its Coordinates
class CoordinatesInline(admin.TabularInline):
    model = CoordinatesModel
    extra = 0


class FieldExpensesInline(admin.TabularInline):
    model = FieldExpenses
    fk_name = 'field'
    extra = 0


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




@admin.register(Expenses)
class ExpensesModelTranslation(admin.ModelAdmin):
    exclude = ('name',)


@admin.register(SugarBeetPointModel)
class SugarBeetPointAdmin(admin.ModelAdmin):
    exclude = ('name',)