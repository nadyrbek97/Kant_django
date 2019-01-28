from django.urls import path, include
from .views import (UserSignUpView,
                    UserLoginView,
                    UserLogoutView,
                    UserChangePasswordView,
                    GetUserByIdView,
                    Test)


urlpatterns = [
    path('user/signup/', UserSignUpView.as_view(), name='user_signup'),
    path('user/login/', UserLoginView.as_view(), name='user_login'),
    path('user/logout/', UserLogoutView.as_view(), name='user_logout'),
    path('user/change-password/<int:pk>/', UserChangePasswordView.as_view(), name='user_change_password'),
    path('user/<int:pk>/', GetUserByIdView.as_view(), name='get_user_by_id'),
    path('user/test/', Test.as_view())

]
