# from modeltranslation.translator import (
#     translator,
#     TranslationOptions,
#     register,
#
# )
#
# from .models import *
#
#
# @register(BankModel)
# class BankModelTranslation(TranslationOptions):
#     fields = ('name', 'description',)
#
#
# @register(BankBranchModel)
# class BankBranchModelTranslation(TranslationOptions):
#     fields = ('name', 'address',)
#
#
# @register(Services)
# class ServicesModelTranslation(TranslationOptions):
#     fields = ('name',)
#
#
# @register(Suppliers)
# class SuppliersModelTranslation(TranslationOptions):
#     fields = ('name',)
#
#
# @register(ContractsModel)
# class ContractsModelTranslation(TranslationOptions):
#     fields = ('title', 'text',)
#
#
# @register(SupplierTypeModel)
# class SupplierTypeModelTranslation(TranslationOptions):
#     fields = ('name', 'description',)
#
#
# @register(SupplierBranchModel)
# class SupplierBranchModelTranslation(TranslationOptions):
#     fields = ('name', 'address',)
#
#
# @register(TechnologyModel)
# class TechnologyModelTranslation(TranslationOptions):
#     fields = ('name', 'text',)
