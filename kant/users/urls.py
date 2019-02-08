from django.urls import path, include
from django.conf.urls import url
from .views import (UserSignUpView,
                    UserLoginView,
                    UserLogoutView,
                    UserChangePasswordView,
                    GetUserByIdView,
                    RegisterUserFirebaseTokenView,
                    DomesticNewsView)


urlpatterns = [
    path('signup/', UserSignUpView.as_view(), name='user_signup'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),
    path('change-password/<int:user_id>/', UserChangePasswordView.as_view(), name='user_change_password'),
    path('<int:pk>/', GetUserByIdView.as_view(), name='get_user_by_id'),


]
