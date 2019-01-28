from django.shortcuts import render

from .models import UserProfile
from .serializers import (UserSignUpSerializer,
                          UserLoginSerializer,
                          UserPasswordChangeSerializer,
                          GetUserByIdSerializer,
                          UpdateUserByIdSerializer
                          )

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication

from django.contrib.auth.models import User
from django.contrib.auth import login as django_login, logout as django_logout
# from django.http import HttpResponse, response

# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


class UserSignUpView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSignUpSerializer

    def post(self, request, *args, **kwargs):
        try:
            if request.data['password'] != request.data['password_repeat']:
                msg = "password doesn't match"
                raise exceptions.ValidationError(msg)
            user = User.objects.create(username=request.data['phone'],
                                       email=request.data['email'])
            serialized = self.get_serializer(data=request.data)
            print(serialized)
            if serialized.is_valid():

                user.set_password(serialized.data["password"])
                user.save()
                UserProfile.objects.create(
                    user=user,
                    phone=request.data['phone'],
                    email=request.data['email'],
                    first_name=request.data['first_name'],
                    last_name=request.data['last_name'],
                    fathers_name=request.data['fathers_name'],
                    date_of_birth=request.data['date_of_birth'],
                    address=request.data['address'],
                    photo=request.data['photo']
                )
                msg = 'Successfully added. '
                return Response(data=msg, status=status.HTTP_201_CREATED)
        except KeyError:
            return Response({"error": "Some error message"}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):

    def post(self, request):
        try:
            serializer = UserLoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            django_login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            context = {}
            context['user_id'] = user.id
            context['token'] = token.key
            return Response(context, status=status.HTTP_200_OK)
        except KeyError:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class UserLogoutView(APIView):
    authentication_classes = (TokenAuthentication, )

    def post(self, request):
        django_logout(request)
        return Response(status=204)


class BearerTokenAuthentication(TokenAuthentication):
    keyword = "Bearer"


class UserChangePasswordView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    # authentication_classes = (BearerTokenAuthentication,)
    serializer_class = UserPasswordChangeSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        print()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if serializer.data.get("new_password") == serializer.data.get("new_password_repeat"):
                msg = " New passwords don't match "
                raise exceptions.ValidationError(msg)
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=400)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response("Success.", status=200)

        return Response(serializer.errors, status=400)


class BearerAuthentication(TokenAuthentication):
    keyword = "Bearer"


class Test(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (BearerAuthentication, )

    def get(self, request):
        test = "This is test"
        return Response(test, status=200)


class GetUserByIdView(APIView):
    # permission_classes = (IsAuthenticated, )
    authentication_classes = (BearerAuthentication, )

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

