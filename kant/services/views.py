from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response

from .serializers import *
from .models import *


class BankView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, *args, **kwargs):

        bank_id = self.kwargs.get('bank_id')
        # print(bank_id)

        if not bank_id:
            banks = BankModel.objects.all()

            if len(banks) > 0:
                banks_serializer = AllBanksSerializer(banks, many=True, )
                return Response(banks_serializer.data, status=status.HTTP_200_OK)
            return Response([], status=status.HTTP_200_OK)
        try:
            bank = BankModel.objects.get(pk=bank_id)
            result = {}

            if bank:
                bank_serializer = BankModelSerializer(bank, many=False)
                # print(bank_serializer.data)
                result['bank_id'] = bank_serializer.data['id']
                result['title'] = bank_serializer.data['name']
                result['logo'] = bank_serializer.data['logo']
                result['description'] = bank_serializer.data['description']

                branches = BankBranchModel.objects.filter(bank=bank_id)
                branches_serializer = BankBranchModelSerializer(branches, many=True)
                result['branches'] = branches_serializer.data
                # print(branches_serializer.data[0])

                contacts = BankContactsModel.objects.all().filter(bank=bank_id)
                contacts_serializer = BankContactsModelSerializer(contacts, many=True)
                result['contacts'] = contacts_serializer.data

                images = BankImagesModel.objects.all().filter(bank=bank_id)
                images_serializer = BankImagesModelSerializer(images, many=True)
                result['images'] = images_serializer.data

                return Response(result, status=status.HTTP_200_OK)

        except BankModel.DoesNotExist:
            return Response([], status=status.HTTP_200_OK)

        return Response({"error": "Bad Request."}, status=status.HTTP_400_BAD_REQUEST)


class ServiceDataView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, *args, **kwargs):
        service_id = self.kwargs.get('data_id')
        banks = BankModel.objects.filter(service_id=service_id)
        banks_serializer = BankModelSerializer(banks, many=True)
        if len(banks_serializer.data) > 0:
            return Response(banks_serializer.data, status=status.HTTP_200_OK)
        return Response([], status=status.HTTP_200_OK)


class ServicesView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, *args, **kwargs):
        service_id = self.kwargs.get('service_id')

        try:
            if service_id:

                service = Services.objects.get(pk=service_id)
                service_serializer = ServicesSerializer(service, many=False)

                return Response(service_serializer.data, status=status.HTTP_200_OK)

            services = Services.objects.all()
            services_serializer = ServicesSerializer(services, many=True)
            result = []

            for s in services_serializer.data:
                data = []
                banks = BankModel.objects.filter(service_id=s['id'])

                for b in banks:
                    bank_result = {}
                    bank_serializer = BankModelSerializer(b, many=False)

                    bank_result['bank_id'] = bank_serializer.data['id']
                    bank_result['title'] = bank_serializer.data['name']
                    bank_result['logo'] = bank_serializer.data['logo']
                    bank_result['description'] = bank_serializer.data['description']

                    branches = BankBranchModel.objects.filter(bank=b)
                    branches_serializer = BankBranchModelSerializer(branches, many=True)
                    bank_result['branches'] = branches_serializer.data

                    contacts = BankContactsModel.objects.all().filter(bank=b)
                    contacts_serializer = BankContactsModelSerializer(contacts, many=True)
                    bank_result['contacts'] = contacts_serializer.data

                    images = BankImagesModel.objects.all().filter(bank=b)
                    images_serializer = BankImagesModelSerializer(images, many=True)
                    bank_result['images'] = images_serializer.data

                    data.append(bank_result)
                result.append({"id": s['id'], "name": s['name'], "logo": s['logo'], "data": data })
            print(result)
            return Response(result, status=status.HTTP_200_OK)
        except Services.DoesNotExist:
            return Response([], status=status.HTTP_200_OK)
        except:
            return Response({"error": "Internal error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SuppliersView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        # language = request.META.get('HTTP_LANGUAGE')
        # language_activate(request, language)
        try:
            supplier_id = self.kwargs.get('supplier_id')
            if supplier_id:
                try:
                    supplier = Suppliers.objects.get(pk=supplier_id)
                    supplier_serializer = SuppliersModelSerializer(supplier, many=False)
                    return Response(supplier_serializer.data,
                                    status=status.HTTP_200_OK)
                except Suppliers.DoesNotExist:
                    return Response([],
                                    status=status.HTTP_200_OK)
            suppliers = Suppliers.objects.all()
            suppliers_serializer = SuppliersModelSerializer(suppliers, many=True)
            result = []
            for data in suppliers_serializer.data:
                array = []
                supplier_type = SupplierTypeModel.objects.filter(suppliers_id=data['id'])
                for supp_pos in supplier_type:
                    supp_serializer = SupplierTypeModelSerializer(supp_pos, many=False, )
                    supp_branch = SupplierBranchModel.objects.filter(supplier_type=supp_pos)
                    supp_branch_serializer = SupplierBranchModelSerializer(supp_branch, many=True, )
                    supp_contacts = SupplierContactsModel.objects.filter(supplier_type=supp_pos)
                    supp_contacts_serializer = SupplierContactsModelSerializer(supp_contacts, many=True, )
                    supp_images = SupplierImagesModel.objects.filter(supplier_type=supp_pos)
                    supp_images_serializer = SupplierImagesModelSerializer(supp_images, many=True, )

                    bank_result = {
                        "id": supp_serializer.data['id'],
                        "title": supp_serializer.data['name'],
                        "logo": supp_serializer.data['logo'],
                        "description": supp_serializer.data['description'],
                        "branches": supp_branch_serializer.data,
                        "contacts": supp_contacts_serializer.data,
                        "images": supp_images_serializer.data
                    }
                    array.append(bank_result)
                result.append({"id": data['id'], "name": data['name'], "logo": data['logo'], "data": array})
            if len(result) > 0:
                return Response(result,
                                status=status.HTTP_200_OK)
            return Response([],
                            status=status.HTTP_200_OK)
        except Services.DoesNotExist:
            return Response([],
                            status=status.HTTP_200_OK)
        except:
            return Response({"error": "Internal error."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
