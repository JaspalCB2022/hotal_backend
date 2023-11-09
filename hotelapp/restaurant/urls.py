from django.urls import path, include
from .views import (
    RestaurantCreateApiView,
    RestaurantUpdateApiView,
    RestaurantDeleteApiView,
    RestaurantListApiView,
)


urlpatterns = [
    path("create/", RestaurantCreateApiView.as_view(), name="create_restaurant"),
    path(
        "update/<int:restaurant_id>/",
        RestaurantUpdateApiView.as_view(),
        name="update_restaurant",
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
    path("inventory/", include("restaurant.Inventory.urls")),
]
