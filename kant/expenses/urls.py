from django.urls import path
from django.conf.urls import url
from .views import (ExpensesView,
                    FieldsView,
                    SugarBeetPointView)

urlpatterns = [
    url(regex='^expenses(?:/(?P<user_id>[0-9]+))?', view=ExpensesView.as_view(), name='expenses-view'),
    path('field/<int:user_id>/', FieldsView.as_view(), name='fields-view'),
    path('beet-point/', SugarBeetPointView.as_view(), name='sugar-beet-point-view'),

]
