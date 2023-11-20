from django.urls import path
from .menuview import MenuTypeListApiView, MenuSubTypeListApiView
from .views import (
    InventoryListApiView,
    InventoryCreateApiView,
    InventoryDeleteApiView,
    RestaurantInventoryListApiView,
    InventoryUpdateApiView,
    InventoryDetailApiView,
)

urlpatterns = [
    path(
        "list/",
        InventoryListApiView.as_view(),
        name="list_restaurant_inventory",
    ),
    path(
        "list/<int:restaurant_id>/<int:table_id>/",
        RestaurantInventoryListApiView.as_view(),
        name="list_inventory_of_restaurant",
    ),
    path(
        "create/",
        InventoryCreateApiView.as_view(),
        name="create_restaurant_inventory",
    ),
    path(
        "delete/<int:inventory_Id>/",
        InventoryDeleteApiView.as_view(),
        name="delete_restaurant_inventory",
    ),
    path(
        "update/<int:inventory_id>/",
        InventoryUpdateApiView.as_view(),
        name="delete_restaurant_inventory",
    ),
    path(
        "detail/<int:inventory_id>/",
        InventoryDetailApiView.as_view(),
        name="inventory_detail_view",
    ),
    path("menutypes/", MenuTypeListApiView.as_view(), name="list_restaurant_menutypes"),
    path("menusubtype/<int:menutype_id>/", MenuSubTypeListApiView.as_view(), name="list_restaurant_menu_sub_type"),
]

