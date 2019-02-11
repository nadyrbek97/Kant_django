from django.urls import path
from django.conf.urls import url

from .views import (BankView,
                    ServicesView,
                    ServiceDataView,
                    SuppliersView,
                    TechnologyView,
                    ContractsView,
                    MainMenuView)

app_name = "services"

urlpatterns = [

    url(regex='^fin-office(?:/(?P<bank_id>[0-9]+))?', view=BankView.as_view(), name='bank-view'),
    url(regex='^service(?:/(?P<service_id>[0-9]+))?', view=ServicesView.as_view(), name='service-view'),
    url(regex='^services-all(?:/(?P<data_id>[0-9]+))?', view=ServiceDataView.as_view(), name='services-data-view'),
    path('supplier', SuppliersView.as_view(), name='suppliers-view'),
    path('technology', TechnologyView.as_view(), name='technology-view'),
    path('contracts',  ContractsView.as_view(), name='contracts-view'),
    path('menu/', MainMenuView.as_view(), name='menu-view'),

    # path('fin-office/<int:bank_id>/', BankView.as_view(), name='bank-view'),
]
