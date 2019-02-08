from rest_framework import serializers
from rest_framework import exceptions
from rest_framework.validators import UniqueValidator, ValidationError
from .models import UserProfile

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import (DomesticNewsModel,
                     DomesticNewsPhotoLink)


class UserSignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False, allow_blank=True, allow_null=True, max_length=100,
                                   validators=[UniqueValidator(queryset=UserProfile.objects.all(),
                                                               message="Почта существует")],
                                   error_messages=(
                                       {
                                           "email": {
                                               "email": "Введите правильный адрес почты"
                                           }
                                       }))
    username = serializers.CharField(required=True, min_length=9,
                                     validators=[UniqueValidator(queryset=User.objects.all(),
                                                                 message="Номер существует")])
    password = serializers.CharField(required=True, min_length=4, error_messages=(
        {
            "password":
                {
                    "required": "Введите пароль",
                    "min_length": "Пароль должен состоять из 4 символов."
                }
        }))

    def create(self, validated_data, *args, **kwargs):
        user = User.objects.create_user(validated_data['username'],
                                        validated_data['email'],
                                        validated_data['password'], )
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email',)

    # password = serializers.CharField(max_length=30)
    # password_repeat = serializers.CharField(max_length=30)
    #
    # class Meta:
    #     model = UserProfile
    #     fields = ['phone', 'email', 'password', 'password_repeat', 'first_name', 'last_name', 'fathers_name',
    #               'date_of_birth', 'address', 'city',  'photo']


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        username = data.get('username', '')
        password = data.get('password', '')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                data['user'] = user
            else:
                msg = 'Unable to login with given credentials'
                raise exceptions.ValidationError(msg)
        else:
            msg = "Must provide correct username and password"
            raise exceptions.ValidationError(msg)

        return data


class ForgotPasswordSerializer(serializers.Serializer):

    phone_number = serializers.CharField(required=True)


class UserPasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_repeat = serializers.CharField(required=True)


class GetUserByIdSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'fathers_name', 'email',
                  'date_of_birth', 'phone', 'city', 'address', 'photo']


class UpdateUserByIdSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'fathers_name', 'email',
                  'date_of_birth', 'phone', 'city', 'address', 'photo']


class UserTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('firebase_token',)


class DomesticNewsModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = DomesticNewsModel
        fields = ('id', 'name', 'description', 'content', 'created', 'updated',)


class DomesticNewsPhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = DomesticNewsPhotoLink
        fields = ('photo_link',)
