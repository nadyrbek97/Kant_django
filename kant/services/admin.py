from django.contrib import admin
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
                     ContractsModel)

admin.site.register(Services)
admin.site.register(BankModel)
admin.site.register(BankBranchModel)
admin.site.register(BankContactsModel)
admin.site.register(BankImagesModel)
admin.site.register(Suppliers)
admin.site.register(SupplierBranchModel)
admin.site.register(SupplierImagesModel)
admin.site.register(SupplierContactsModel)
admin.site.register(SupplierTypeModel)
admin.site.register(TechnologyModel)
admin.site.register(ContractsModel)
