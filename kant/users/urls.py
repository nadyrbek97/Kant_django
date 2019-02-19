from django.urls import path, include
from django.conf.urls import url
from django.conf.urls import url
from .views import (UserSignUpView,
                    UserLoginView,
                    UserLogoutView,
                    UserChangePasswordView,
                    GetUserByIdView,
                    UserView,
                    DomesticNewsView)


urlpatterns = [
    path('signup', UserSignUpView.as_view(), name='user_signup'),
    path('login', UserLoginView.as_view(), name='user_login'),
    path('logout', UserLogoutView.as_view(), name='user_logout'),
    url(regex='^change-password/(?P<user_id>[0-9]+)', view=UserChangePasswordView.as_view(), name='change-password'),
    url(regex='^(?P<user_id>[0-9]+)', view=UserView.as_view(), name='user-data-view'),
    path('<int:pk>', GetUserByIdView.as_view(), name='get_user_by_id'),


]
