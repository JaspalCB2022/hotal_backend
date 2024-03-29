from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)
from .views import CurrentUserApiView, GetAllKitchenUserApiView, ResetPasswordAPIView, ForgotPasswordApiView ,CreateKitchenUserAPIView, UpdateKitcheStaffUserApiView, KitcheStaffChangePasswordAPIView, KitchenStaffDeleteAPIView

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", TokenBlacklistView.as_view(), name="logout_view"),
    path("user/", CurrentUserApiView.as_view(), name="current_user"),
    path("password/forgot/", ForgotPasswordApiView.as_view(), name="forgot_password"),
    path(
        "password/change/<str:token>/",
        ResetPasswordAPIView.as_view(),
        name="reset_password",
    ),
    path('add/kitchenstaff/',CreateKitchenUserAPIView.as_view(), name='add_kitchen_staff'),
    path('update/kitchenstaff/<int:userid>/',UpdateKitcheStaffUserApiView.as_view(), name='update_kitchen_staff'),
    path('changepassword/kitchenstaff/',KitcheStaffChangePasswordAPIView.as_view(), name='change_password_kitchen_staff'),
    path('all/kitchenstaff/', GetAllKitchenUserApiView.as_view(),name='all_kitchen_staff'),
    path('delete/kitchenstaff/<int:pk>/', KitchenStaffDeleteAPIView.as_view(), name='delete_Kitchen_staff'),
]
