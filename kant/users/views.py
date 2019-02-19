from urllib.request import urlopen, Request

from rest_framework.pagination import LimitOffsetPagination

from .models import UserProfile, DomesticNewsModel, DomesticNewsPhotoLink, UserImageField
from .serializers import (UserSignUpSerializer,
                          UserImageFieldSerializer,
                          UserLoginSerializer,
                          UserPasswordChangeSerializer,
                          GetUserByIdSerializer,
                          UserProfileSerializer,
                          UpdateUserByIdSerializer,
                          UserTokenSerializer,
                          ForgotPasswordSerializer, DomesticNewsModelSerializer, DomesticNewsPhotoSerializer)

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions
from rest_framework.validators import ValidationError

from django.contrib.auth.models import User
from django.contrib.auth import login as django_login, logout as django_logout, authenticate as django_authenticate
from django.utils import translation
from rest_framework.permissions import IsAuthenticated

from parsing.methods import language_activate

import json, traceback

from decouple import config


class UserSignUpView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        try:
            user_data = {
                "username": request.data['phone'],
                "email": request.data['email'],
                "password": request.data['password']
            }

            serializer = UserSignUpSerializer(data=user_data, many=False)
            if serializer.is_valid():
                if request.data['password'] != request.data['password_repeat']:
                    return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)
                user = serializer.save()
                # print(user)

                try:
                    user_profile = UserProfile.objects.create(user=user)
                    user_profile.first_name = request.data['first_name']
                    user_profile.last_name = request.data['last_name']
                    user_profile.fathers_name = request.data['fathers_name']
                    user_profile.email = request.data['email']
                    user_profile.phone = request.data['phone']
                    user_profile.list_phones = [request.data['phone']]
                    user_profile.date_of_birth = request.data['date_of_birth']

                    if 'city' in request.data:
                        user_profile.city = request.data['city']

                    if 'address' in request.data:
                        user_profile.address = request.data['address']

                    if 'photo' in request.data:
                        user_profile.photo = request.data['photo']

                    user_profile.firebase_token = ""
                    user_profile.save()
                    # print(user_profile)

                    dat = json.dumps({
                        "username": request.data['phone'],
                        "password": request.data['password']
                    })

                    req = Request(config('HOST_URL')+ '/api/token-auth', bytes(dat, encoding="utf-8"),
                                  {'Content-Type': 'application/json'})

                    response_body = urlopen(req)
                    data = response_body.read()
                    encoding = response_body.info().get_content_charset('utf-8')
                    result = json.loads(data.decode(encoding))
                    user = django_authenticate(username=request.data['phone'],
                                               password=request.data['password'])

                    django_login(request, user)

                    result_data = {
                        "user_id": user.id,
                        "token": result['token']
                    }

                    return Response(result_data, status=status.HTTP_200_OK)
                except ValidationError:
                    user.delete()
                    return Response({"error": "Invalid user profile data."}, status=status.HTTP_400_BAD_REQUEST)
                except KeyError:
                    user.delete()
                    return Response({"error": KeyError}, status=status.HTTP_400_BAD_REQUEST)
                except:
                    user.delete()
                    traceback.print_stack()
                    return Response({"error": "Uncaught error occured."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            user.delete()
            return Response({"error": KeyError}, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        language = request.META.get('HTTP_LANGUAGE')
        language_activate(request, language)
        try:
            user_id = self.kwargs.get('user_id')
            user = UserProfile.objects.get(user_id=user_id, )
            user_serializer = UserProfileSerializer(user, many=False, )
            return Response(user_serializer.data,
                            status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({"error": "User with given ID not found."},
                            status=status.HTTP_404_NOT_FOUND)
        except KeyError:
            return Response({"error": "User ID key error occured. Please enter valid user ID"},
                            status=status.HTTP_400_BAD_REQUEST)
        except AttributeError:
            return Response({"error": "User ID error. Invalid user ID."},
                            status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error": "Uncaught internal server error."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, *args, **kwargs):
        try:
            user_id = self.kwargs.get('user_id')
            user = UserProfile.objects.get(user_id=user_id)
            user_serializer = UserProfileSerializer(user,
                                                    data=request.data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response(user_serializer.data,
                                status=status.HTTP_202_ACCEPTED)
            return Response({"error": "Bad request data."},
                            status=status.HTTP_400_BAD_REQUEST)
        except UserProfile.DoesNotExist:
            return Response({"error": "User with given ID not found."},
                            status=status.HTTP_404_NOT_FOUND)
        except KeyError:
            return Response({"error": "User ID key error occured. Please enter valid user ID"},
                            status=status.HTTP_400_BAD_REQUEST)
        except AttributeError:
            return Response({"error": "User ID error. Invalid user ID."},
                            status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error": "Uncaught internal server error."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)



import base64
from django.core.files.base import ContentFile


class UserImageFieldView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        try:
            uimodel = UserImageField.objects.all()
            serializer = UserImageFieldSerializer(uimodel, many=True)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        except:
            return Response({"error": "Internal server error."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):

        data = request.data
        image = data['image']
        img = ContentFile(base64.b64decode(str(image)))
        res = {
            'name': data['name'],
            'image': img
        }
        serializer = UserImageFieldSerializer(data=res)
        if serializer.is_valid():
            serializer.save()
        return Response({"error": serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        data = request.data
        print(request.data)
        username = data.get('phone', None)
        password = data.get('password', None)
        dat = json.dumps({
            "username": username,
            "password": password
        })
        try:
            req = Request(config('HOST_URL') + '/api/token-auth', bytes(dat, encoding="utf-8"),
                          {'Content-Type': 'application/json'})
            req.data
            response_body = urlopen(req)
            data = response_body.read()
            encoding = response_body.info().get_content_charset('utf-8')
            result = json.loads(data.decode(encoding))
            user = django_authenticate(username=username, password=password)
            if user is not None:
                django_login(request, user)
                result_data = {
                    "user_id": user.id,
                    "token": result['token']
                }
                return Response(result_data,
                                status=status.HTTP_200_OK)
            return Response({"error": "User not found."},
                            status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"error": 'User does not exist.'},
                            status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({"error": "Incorrect username or password"},
                            status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    authentication_classes = (TokenAuthentication, )

    def post(self, request):
        django_logout(request)
        return Response(status=204)


class BearerTokenAuthentication(TokenAuthentication):
    keyword = "Bearer"


class UserChangePasswordView(generics.UpdateAPIView):
    serializer_class = UserPasswordChangeSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        user_id = self.kwargs.get('user_id')
        obj = User.objects.get(pk=user_id)
        return obj

    def update(self, request, *args, **kwargs):
        language = request.META.get('HTTP_LANGUAGE')
        language_activate(request, language)
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"password": ["Неправильный пароль"]},
                                status=status.HTTP_400_BAD_REQUEST)
            if len(request.data['new_password']) < 4:
                return Response({"password": "Ваш пароль должен состоять из четырёх символов."})
            if serializer.data.get("new_password") != serializer.data.get("new_password_repeat"):
                return Response({"error": "Новые пароли не совпадают"},
                                status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            if request.session[translation.LANGUAGE_SESSION_KEY] == 'kg':
                return Response("Паролингыз озгорду", status=status.HTTP_200_OK)
            return Response("Ваш пароль был успешно изменён")

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BearerAuthentication(TokenAuthentication):
    keyword = "Bearer"


class Test(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (BearerAuthentication, )

    def get(self, request):
        test = "This is test"
        return Response(test, status=200)


class GetUserByIdView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):

        try:
            user_id = kwargs['pk']
            user = UserProfile.objects.get(user=user_id)
            user_serializer = GetUserByIdSerializer(user, many=False)
            return Response(user_serializer.data,
                            status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({"error": "User with given ID not found."})
        except KeyError:
            return Response({"error": "User ID key error occured. Please enter valid user ID."})
        except AttributeError:
            return Response({"error": "User ID error. Invalid user ID."})
        except:
            return Response({"error": "Uncaught internal sever error"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, *args, **kwargs):

        try:
            user_id = kwargs['pk']
            user = UserProfile.objects.get(user=user_id)
            user_serializer = GetUserByIdSerializer(user, data=request.data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response(user_serializer.data,
                                status=status.HTTP_202_ACCEPTED)
            return Response({"error": "Bad request data."},
                            status=status.HTTP_400_BAD_REQUEST)
        except UserProfile.DoesNotExist:
            return Response({"error": "User with given ID not found"},
                            status=status.HTTP_404_NOT_FOUND)
        except KeyError:
            return Response({"error": "User ID key error occured. Please enter valid user ID."},
                            status=status.HTTP_400_BAD_REQUEST)
        except AttributeError:
            return Response({"error": "User ID error. Invalid user ID."},
                            status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error": "Uncaught internal sever error"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#
# class SendFirebaseMessageView(APIView):
#     permission_classes = (permissions.AllowAny,)
#
#     def get(self, request, *args, **kwargs):
#         # Device = get_device_model()
#         # print(GCMDevice.objects.all())
#         devices = GCMDevice.objects.all()
#         # Device.objects.all().send_message({'message': 'my test message'})
#         print(devices.send_message(
#             "This is a message",
#             extra={
#                 "notification": {
#                     "title": "Notification title",
#                     "body": ""
#                 },
#                 "content_available": True,
#                 "priority": "high",
#             }))
#         # my_phone = Device.objects.all()
#         # my_phone.send_message({'message': 'my test message'}, collapse_key='something')
#         return Response([], status=status.HTTP_200_OK)


# class SendFirebase(APIView):
#     permission_classes = (permissions.AllowAny,)
#
#     def get(self, request, *args, **kwargs):
#         tokens = UserProfile.objects.values_list('firebase_token')
#         print(tokens[0])
#         params = {}
#         params['title'] = "Manchester United - Liverpool"
#         params['body'] = "0 : 7"
#         params['sound'] = "default"
#
#         values = {
#             'content-available': True,
#             'PATCHpriority': 'high',
#             # 'to': '/topics/domestic_news',
#             "registration_ids": [item[0] for item in tokens],
#             'notification': params
#         }
#
#         headers = {
#             'Content-Type': 'application/json',
#             'Authorization': 'key=' + config('FCM_API')
#         }
#         print(headers['Authorization'])
#
#         return Response(
#             requests.post(url="https://fcm.googleapis.com/fcm/send", data=json.dumps(values), headers=headers),
#             status=status.HTTP_200_OK)
#
#
# class RegisterUserFirebaseTokenView(APIView):
#     permission_classes = (permissions.IsAuthenticated,)
#
#     def patch(self, request, *args, **kwargs):
#         try:
#             user_id = self.kwargs.get('user_id')
#             user = UserProfile.objects.get(user_id=user_id)
#             user_serializer = UserTokenSerializer(user,
#                                                   data=request.data)
#             print(user_serializer)
#             if user_serializer.is_valid():
#                 user_serializer.save()
#                 return Response({"User token successfully changed or added."},
#                                 status=status.HTTP_200_OK)
#             return Response({"error": "Bad Request Data"},
#                             status=status.HTTP_400_BAD_REQUEST)
#         except UserProfile.DoesNotExist:
#             return Response({"error": "User with given ID not found."},
#                             status=status.HTTP_404_NOT_FOUND)
#         except KeyError:
#             return Response({"error": "Bad Request Data"},
#                             status=status.HTTP_400_BAD_REQUEST)
#         except:
#             return Response({"error": "Uncaught internal server error."},
#                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DomesticNewsView(APIView):
    permission_classes = (permissions.AllowAny,)
    queryset = DomesticNewsModel.objects.all().order_by('-id')
    serializer_class = DomesticNewsModelSerializer
    pagination_class = LimitOffsetPagination

    def get(self, request, *args, **kwargs):
        language = request.META.get('HTTP_LANGUAGE')
        language_activate(request, language)
        page = self.paginate_queryset(self.queryset)
        if len(page) > 0:
            serializer = self.serializer_class(page, many=True)
            result = []
            data = {}
            for item in serializer.data:
                photo = DomesticNewsPhotoLink.objects.filter(domestic_id=item['id'])
                photo_serializer = DomesticNewsPhotoSerializer(photo, many=True, )
                data['news'] = item
                data['photos'] = photo_serializer.data
                result.append(data)
                data = {}

            return self.get_paginated_response(result)  # serializer.data)

        return Response([], status=status.HTTP_200_OK)


    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)
