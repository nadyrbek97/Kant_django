from django.contrib import admin

from .models import (Expenses,
                     FieldsModel,
                     SugarBeetPointModel,
                     FieldExpenses,
                     )

admin.site.register(Expenses)
admin.site.register(FieldsModel)
admin.site.register(SugarBeetPointModel)
admin.site.register(FieldExpenses)