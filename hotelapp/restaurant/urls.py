from django.urls import path, include
from .views import (
    RestaurantCreateApiView,
    RestaurantUpdateApiView,
    RestaurantDeleteApiView,
    RestaurantListApiView,
    TableCreateApiView,
    TableListApiView,
    RestaurantDetailApiView,
    RestaurantUpdateOwnProfile,
    TableQRCodeView
)


urlpatterns = [
    path(
        "create/",
        RestaurantCreateApiView.as_view(),
        name="create_restaurant",
    ),
    path(
        "update/<int:restaurant_id>/",
        RestaurantUpdateApiView.as_view(),
        name="update_restaurant",
    ),
    path(
        "update/own/profile/",
        RestaurantUpdateOwnProfile.as_view(),
        name="update_own_profile",
    ),
    path(
        "delete/<int:restaurant_id>/",
        RestaurantDeleteApiView.as_view(),
        name="delete_restaurant",
    ),
    path(
        "list/",
        RestaurantListApiView.as_view(),
        name="delete_retaurant",
    ),
    path(
        "detail/<int:restaurant_id>/",
        RestaurantDetailApiView.as_view(),
        name="restaurant_detail_view",
    ),
    path("inventory/", include("restaurant.Inventory.urls")),
    path("createtable/", TableCreateApiView.as_view(), name="create_table"),
    path("tables/", TableListApiView.as_view(), name="tables_list"),
    path('table/<int:table_id>/qr-code/', TableQRCodeView.as_view(), name='table-qr-code'),

]
