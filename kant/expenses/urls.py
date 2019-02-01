from django.urls import path
from .views import (ExpensesView,
                    FieldsView,
                    SugarBeetPointView)

urlpatterns = [
    path('expenses/<int:field_id>/', ExpensesView.as_view(), name='expenses-view'),
    path('field/<int:user_id>/', FieldsView.as_view(), name='fields-view'),
    path('beet-point/', SugarBeetPointView.as_view(), name='sugar-beet-point-view'),

]
