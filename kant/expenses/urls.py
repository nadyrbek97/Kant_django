from django.urls import path
from .views import (ExpensesView,
                    FieldsView)

urlpatterns = [
    path('expenses/<int:field_id>/', ExpensesView.as_view(), name='expenses-view'),
    path('field/<int:user_id>/', FieldsView.as_view(), name='fields-view'),

]
