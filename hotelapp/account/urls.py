from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
    
)
from .views import ListUserApiView,ResetPasswordAPIView,ForgotPasswordApiView

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", TokenBlacklistView.as_view(), name="logout_view"),
    path("list/", ListUserApiView.as_view(), name="list_user"),
    path("password/forgot/",ForgotPasswordApiView.as_view(),name='forgot_password'),
    path("password/change/<str:token>/",ResetPasswordAPIView.as_view(),name="reset_password")
]