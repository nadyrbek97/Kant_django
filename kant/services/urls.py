from django.urls import path
from django.conf.urls import url

from .views import (BankView,)

urlpatterns = [

    url(regex='^fin-office(?:/(?P<bank_id>[0-9]+))?', view=BankView.as_view(), name='bank-view'),
    # path('fin-office/<int:bank_id>/', BankView.as_view(), name='bank-view'),
]
