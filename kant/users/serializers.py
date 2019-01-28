from rest_framework import serializers
from rest_framework import exceptions

from .models import UserProfile

from django.contrib.auth import authenticate, login


class UserSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=30)
    password_repeat = serializers.CharField(max_length=30)

    class Meta:
        model = UserProfile
        fields = ['phone', 'email', 'password', 'password_repeat', 'first_name', 'last_name', 'fathers_name',
                  'date_of_birth', 'address', 'city',  'photo']


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


class UserPasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    new_password_repeat = serializers.CharField


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
