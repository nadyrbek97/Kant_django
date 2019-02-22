"""kant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from rest_framework_jwt.views import (obtain_jwt_token,
                                      verify_jwt_token,
                                      refresh_jwt_token)
from users.views import RegisterUserFirebaseTokenView
from rest_framework.routers import DefaultRouter
from fcm_django.api.rest_framework import FCMDeviceViewSet, FCMDeviceAuthorizedViewSet
from users.views import UserImageFieldView

router = DefaultRouter()
router.register(r'devices', FCMDeviceViewSet)
router.register(r'register', FCMDeviceAuthorizedViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token-auth', obtain_jwt_token, name="ApiTokenAuthentication"),
    path('api/token-refresh', refresh_jwt_token, name="ApiTokenRefresh"),
    path('api/token-verify', verify_jwt_token, name='ApiTokenVerify'),
    path('api/user/', include('users.urls')),
    path('api/image', UserImageFieldView.as_view(), name='image-view'),
    path('api/', include('parsing.urls')),
    path('api/', include('expenses.urls')),
    path('api/', include('services.urls')),
    path('firebase/', include(router.urls)),
    url(regex='^api/user/register-token/(?P<user_id>[0-9]+)', view=RegisterUserFirebaseTokenView.as_view(), name='firebase-token-register-view'),

]
