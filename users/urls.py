from django.urls import path
from rest_framework.permissions import AllowAny
from users.apps import UsersConfig
from users.views import UserCreateAPIView, \
    UserRetrieveAPIView, UserUpdateAPIView, UserDestroyAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


app_name = UsersConfig.name


urlpatterns = [
    path('register/', UserCreateAPIView.as_view(permission_classes=(AllowAny,)), name='register'),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
    path('user_detail/<int:pk>/', UserRetrieveAPIView.as_view(), name='user_detail'),
    path('user_update/<int:pk>/', UserUpdateAPIView.as_view(), name='user_update'),
    path('user_delete/<int:pk>/', UserDestroyAPIView.as_view(), name='user_delete'),
]
